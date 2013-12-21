import collections
import colander
import json


def valid_key(key):
    if key:
        return key
    return False


class SchemaAdapterMixin(object):

    def from_request(self, args=None, kwargs=None, query_dict=None, request_json=None, key_prefix=None):
        list_args = []
        redis_args = []
        redis_kwargs = []
        names = []
        for node in self.children:
            names.append(node.name)
            if isinstance(node.typ, colander.Sequence):
                list_args.append(node.name)

            if node.required:
                redis_args.append(node.name)
            else:
                redis_kwargs.append(node.name)

        cstruct = dict(zip(names, args))
        for arg in redis_args:
            if query_dict.get(arg):
                cstruct[arg] = query_dict.get(arg)

        for arg in redis_kwargs:
            if query_dict.get(arg):
                cstruct[arg] = query_dict.get(arg)

        if kwargs:
            cstruct.update(kwargs)

        if request_json:
            cstruct.update(request_json)

        for name in list_args:
            if query_dict.getlist(name):
                cstruct[name] = query_dict.getlist(name)

        # print "Going to deserialize: %s" % (cstruct)
        schema_instance = self.clone()
        schema_instance.redis_prefix = key_prefix
        data = schema_instance.deserialize(cstruct)
        # print "deserialized data: %s redis_args: %s redis_kwargs: %s" % (data, redis_args, redis_kwargs)
        args, kwargs = schema_instance.signature_from_cstruct(data, redis_args, redis_kwargs)

        return (args, kwargs)

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        args = [cstruct[arg] for arg in redis_args]
        kwargs = dict((arg, cstruct.get(arg)) for arg in redis_kwargs)
        return (args, kwargs)


class StringBool(colander.Bool):
    def __init__(self, default=False):
        self.default = default

    def deserialize(self, node, cstruct):
        if not cstruct:
            return self.default

        cstruct = unicode(cstruct)
        cstruct = cstruct.lower()

        if cstruct == 'true' or cstruct == '1':
            return True

        if cstruct == 'false' or cstruct == '0':
            return False

        return self.default


# Our strings can be a blank value
# They can be integers
# Whatever we get returned from redis is what we want to transmit
class LarkString(colander.String):

    def deserialize(self, node, cstruct):
        if cstruct == '':
            return cstruct

        if isinstance(cstruct, basestring):
            return cstruct

        if isinstance(cstruct, int) or isinstance(cstruct, float):
            return unicode(cstruct)

        return super(LarkString, self).deserialize(node, cstruct)

    def serialize(self, node, appstruct):
        return appstruct


# This is a type that is a reference in to a key, or name in redis.
# So, this would
class RedisReferenceType(LarkString):
    pass


# This is a type that is a reference in to a key, or name in redis.
# So, this would
class BinaryValueType(LarkString):
    def deserialize(self, node, cstruct):
        cstruct = super(BinaryValueType, self).deserialize(node, cstruct)
        return cstruct.decode('base64')

    def serialize(self, node, appstruct):
        return appstruct.encode('base64')


# For some keys in redis I want to be able to prefix them transparently from the user
# That way many users can share the same redis DB
class PrefixedRedisReferenceType(RedisReferenceType):
    def deserialize(self, node, cstruct):
        cstruct = super(PrefixedRedisReferenceType, self).deserialize(node, cstruct)
        if not cstruct:
            return cstruct

        prefix = getattr(node, 'redis_prefix', None)

        if prefix:
            cstruct = u'%s:%s' % (prefix, cstruct)

        return cstruct

    def serialize(self, node, appstruct):
        appstruct = super(PrefixedRedisReferenceType, self).serialize(node, appstruct)
        prefix = getattr(node, 'redis_prefix', None)
        if prefix and appstruct.startswith(prefix):
            appstruct = appstruct.replace(prefix + ':', '', 1)

        return appstruct


# Turn any incoming value into JSON
# Turn any outgoing value into python
class RedisValueType(LarkString):
    def deserialize(self, node, cstruct):
        if cstruct is not None:
            if isinstance(cstruct, basestring):
                return cstruct

            if isinstance(cstruct, dict) or isinstance(cstruct, collections.Iterable):
                cstruct = json.dumps(cstruct)

            return cstruct

        return super(RedisValueType, self).deserialize(node, cstruct)

    def serialize(self, node, appstruct):
        if not appstruct:
            return appstruct

        if appstruct == '':
            return appstruct

        if not isinstance(appstruct, basestring):
            return appstruct

        if appstruct[0] != '{':
            return appstruct

        return json.loads(appstruct)


# Noop type just returns the app struct it's handed
class NoopType(colander.SchemaType):
    def serialize(self, node, appstruct):
        return appstruct

    def deserialize(self, node, cstruct):
        return cstruct


# Outbound types for things from redis to the user
class OutboundType(colander.Mapping):
    def __init__(self, *args, **kwargs):
        super(OutboundType, self).__init__(unknown='preserve')


class OutboundMappingSchema(colander.MappingSchema):
    schema_type = OutboundType


class OutboundSequenceSchema(colander.SequenceSchema):
    value = colander.SchemaNode(RedisValueType())


OutboundValueSchema = colander.SchemaNode(RedisValueType())
OutboundResultSchema = colander.SchemaNode(NoopType())
OutBoundBinaryValueSchema = colander.SchemaNode(BinaryValueType())


class OutboundKeyValueListSchema(colander.TupleSchema):
    name = colander.SchemaNode(RedisReferenceType())
    value = colander.SchemaNode(RedisValueType())


# Schema
class OutboundValueListSchema(colander.SequenceSchema):
    value = OutboundValueSchema


# Scheam
class OutboundSortSchema(colander.Schema):
    schema_type = NoopType

    def serialize(self, node, appstruct):
        if len(appstruct) == 0:
            return appstruct

        if isinstance(appstruct[0], collections.Iterable):
            return OutboundKeyValueListSchema().serialize(appstruct)
        else:
            return OutboundValueListSchema().serialize(appstruct)


# Type
class LarkMappingSchema(colander.Mapping):
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        def callback(subnode, subappstruct):
            subnode.redis_prefix = node.redis_prefix
            return subnode.serialize(subappstruct)

        return self._impl(node, appstruct, callback)

    def deserialize(self, node, cstruct, accept_scalar=None):
        if cstruct is colander.null:
            return colander.null

        def callback(subnode, subcstruct):
            subnode.redis_prefix = node.redis_prefix
            return subnode.deserialize(subcstruct)

        return self._impl(node, cstruct, callback)


# Type
class LarkSequenceSchema(colander.Sequence):
    def serialize(self, node, appstruct, accept_scalar=None):
        if appstruct is colander.null:
            return colander.null

        def callback(subnode, subappstruct):
            subnode.redis_prefix = node.redis_prefix
            return subnode.serialize(subappstruct)

        return self._impl(node, appstruct, callback, accept_scalar)

    def deserialize(self, node, cstruct, accept_scalar=None):
        if cstruct is colander.null:
            return colander.null

        def callback(subnode, subcstruct):
            subnode.redis_prefix = node.redis_prefix
            return subnode.deserialize(subcstruct)

        return self._impl(node, cstruct, callback, accept_scalar)


class LarkSchemaNode(SchemaAdapterMixin, colander.SchemaNode):
    pass

lark_string = LarkString()
ref_type = RedisReferenceType()
name_ref_type = PrefixedRedisReferenceType()
value_type = RedisValueType()
int_type = colander.Integer()
float_type = colander.Float()
bool_type = colander.Boolean()
datetime_type = colander.DateTime()
string_bool = StringBool()
bin_type = BinaryValueType()


def node(schema, *args, **kwargs):
    schema.add(colander.SchemaNode(*args, **kwargs))


NameValueTupleSchema = colander.SchemaNode(colander.Tuple())
NameValueTupleSchema.add(colander.SchemaNode(name_ref_type, name='name'))
NameValueTupleSchema.add(colander.SchemaNode(value_type, name='value'))


class NameValueListSchemaNode(LarkSchemaNode):

    def from_request(self, args=None, kwargs=None, query_dict=None, request_json=None, redis_prefix=None):
        cstruct = {
            'value': request_json
        }
        # print "Going to deserialize: %s" % (cstruct)
        self.redis_prefix = redis_prefix
        data = self.deserialize(cstruct)
        args, kwargs = self.signature_from_cstruct(data)

        return (args, kwargs)

    def signature_from_cstruct(self, cstruct):
        values = cstruct['value']
        return ([], dict(values))


NameValueListSchema = NameValueListSchemaNode(LarkMappingSchema())
NameValueListSchema.add(LarkSchemaNode(colander.Sequence(), NameValueTupleSchema, name='value'))


NameScoreTupleSchema = colander.SchemaNode(colander.Tuple())
NameScoreTupleSchema.add(colander.SchemaNode(lark_string, name='name'))
NameScoreTupleSchema.add(colander.SchemaNode(lark_string, name='score'))


class NameScoreListSchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        name = cstruct['name']
        scores = cstruct['scores']
        return ([name], dict(scores))


NameScoreListSchema = NameScoreListSchemaNode(LarkMappingSchema())
NameScoreListSchema.add(LarkSchemaNode(name_ref_type, name='name'))
NameScoreListSchema.add(LarkSchemaNode(colander.Sequence(), NameValueTupleSchema, name='scores'))


NoSchema = LarkSchemaNode(LarkMappingSchema())


AddressSchema = LarkSchemaNode(LarkMappingSchema())
node(AddressSchema, lark_string, name='address')


InfotypeKeyScheam = LarkSchemaNode(LarkMappingSchema())
node(InfotypeKeyScheam, lark_string, name='infotype')
node(InfotypeKeyScheam, name_ref_type, name='key')


NameSchema = LarkSchemaNode(LarkMappingSchema())
node(NameSchema, name_ref_type, name='name')


class NamesSchemaNode(LarkSchemaNode):
    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        return (cstruct['name'], {})


NamesSchema = NamesSchemaNode(LarkMappingSchema())
NamesSchema.add(LarkSchemaNode(colander.Sequence(accept_scalar=True), LarkSchemaNode(name_ref_type), name='name'))


PatternSchema = LarkSchemaNode(LarkMappingSchema())
node(PatternSchema, name_ref_type, name='pattern', missing='*')

KeySchema = LarkSchemaNode(LarkMappingSchema())
node(KeySchema, name_ref_type, name='key')


class KeySchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        return (cstruct['key'], {})


KeysSchema = KeySchemaNode(LarkMappingSchema())
KeysSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(name_ref_type), name='key'))

KeyListSchema = LarkSchemaNode(LarkMappingSchema())
KeyListSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(name_ref_type), name='key'))

KeysTimeoutSchema = LarkSchemaNode(LarkMappingSchema())
KeysTimeoutSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(name_ref_type), name='keys'))
node(KeysTimeoutSchema, int_type, name='timeout')

ValueSchema = LarkSchemaNode(LarkMappingSchema())
node(ValueSchema, value_type, name='value')


NameAmountSchema = LarkSchemaNode(LarkMappingSchema())
node(NameAmountSchema, name_ref_type, name='name')
node(NameAmountSchema, name_ref_type, name='amount', missing=1)

NameFloatAmountSchema = LarkSchemaNode(LarkMappingSchema())
node(NameFloatAmountSchema, name_ref_type, name='name')
node(NameFloatAmountSchema, float_type, name='amount', missing=1.0)


SectionSchema = LarkSchemaNode(LarkMappingSchema())
node(SectionSchema, lark_string, name='section', missing=None)


NameTimeSchema = LarkSchemaNode(LarkMappingSchema())
node(NameTimeSchema, name_ref_type, name='name')
node(NameTimeSchema, int_type, missing=None, name='time')


NameValueTimeSchema = LarkSchemaNode(LarkMappingSchema())
node(NameValueTimeSchema, name_ref_type, name='name')
node(NameValueTimeSchema, value_type, name='value')
node(NameValueTimeSchema, int_type, name='time')


NameTimeMsValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameTimeMsValueSchema, name_ref_type, name='name')
node(NameTimeMsValueSchema, int_type, name='time_ms')
node(NameTimeMsValueSchema, value_type, name='value')


NameOffsetSchema = LarkSchemaNode(LarkMappingSchema())
node(NameOffsetSchema, name_ref_type, name='name')
node(NameOffsetSchema, int_type, name='offset')


NameOffsetBoolValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameOffsetBoolValueSchema, name_ref_type, name='name')
node(NameOffsetBoolValueSchema, int_type, name='offset')
node(NameOffsetBoolValueSchema, bool_type, name='value')


NameOffsetStrValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameOffsetStrValueSchema, name_ref_type, name='name')
node(NameOffsetStrValueSchema, int_type, name='offset')
node(NameOffsetStrValueSchema, lark_string, name='value')


NameValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameValueSchema, name_ref_type, name='name')
node(NameValueSchema, value_type, name='value')


class NameValuesSchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        name = cstruct['name']
        values = cstruct['values']
        return ([name] + values, {})


NameValuesSchema = NameValuesSchemaNode(LarkMappingSchema())
node(NameValuesSchema, name_ref_type, name='name')
NameValuesSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(value_type), name='values'))


class RemNameValueListSchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        name = cstruct['name']
        values = cstruct['value']
        return ([name] + values, {})


RemNameValueListSchema = RemNameValueListSchemaNode(LarkMappingSchema())
node(RemNameValueListSchema, name_ref_type, name='name')
RemNameValueListSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(value_type), name='value'))


NameWhenSchema = LarkSchemaNode(LarkMappingSchema())
node(NameWhenSchema, name_ref_type, name='name')
node(NameWhenSchema, datetime_type, name='when')


KeyValueSchema = LarkSchemaNode(LarkMappingSchema())
node(KeyValueSchema, name_ref_type, name='key')
node(KeyValueSchema, value_type, name='value')


SetSchema = LarkSchemaNode(LarkMappingSchema())
node(SetSchema, name_ref_type, name='key')
node(SetSchema, value_type, name='value')
node(SetSchema, int_type, name='ex', missing=None)
node(SetSchema, int_type, name='px', missing=None)
node(SetSchema, bool_type, name='nx', missing=False)
node(SetSchema, bool_type, name='xx', missing=False)


KeyRangeSchema = LarkSchemaNode(LarkMappingSchema())
node(KeyRangeSchema, name_ref_type, name='key')
node(KeyRangeSchema, int_type, name='start')
node(KeyRangeSchema, int_type, name='end')


KeyRangeOptionalSchema = LarkSchemaNode(LarkMappingSchema())
node(KeyRangeOptionalSchema, name_ref_type, name='key')
node(KeyRangeOptionalSchema, int_type, name='start', missing=None)
node(KeyRangeOptionalSchema, int_type, name='end', missing=None)


NameRangeSchema = LarkSchemaNode(LarkMappingSchema())
node(NameRangeSchema, name_ref_type, name='name')
node(NameRangeSchema, int_type, name='start')
node(NameRangeSchema, int_type, name='end')


NameRangeEndOptionalSchema = LarkSchemaNode(LarkMappingSchema())
node(NameRangeEndOptionalSchema, name_ref_type, name='name')
node(NameRangeEndOptionalSchema, int_type, name='start')
node(NameRangeEndOptionalSchema, int_type, name='end', missing=-1)


SrcDstSchema = LarkSchemaNode(LarkMappingSchema())
node(SrcDstSchema, name_ref_type, name='src')
node(SrcDstSchema, name_ref_type, name='dst')


SrcDstValueSchema = LarkSchemaNode(LarkMappingSchema())
node(SrcDstValueSchema, name_ref_type, name='src')
node(SrcDstValueSchema, name_ref_type, name='dst')
node(SrcDstValueSchema, value_type, name='value')


SrcDstTimeoutSchema = LarkSchemaNode(LarkMappingSchema())
node(SrcDstTimeoutSchema, name_ref_type, name='src')
node(SrcDstTimeoutSchema, name_ref_type, name='dst')
node(SrcDstTimeoutSchema, int_type, name='timeout', missing=0)


NameIndexSchema = LarkSchemaNode(LarkMappingSchema())
node(NameIndexSchema, name_ref_type, name='name')
node(NameIndexSchema, int_type, name='index')


NameNumValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameNumValueSchema, name_ref_type, name='name')
node(NameNumValueSchema, int_type, name='num', missing=0)
node(NameNumValueSchema, value_type, name='value')


NameIndexValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameIndexValueSchema, name_ref_type, name='name')
node(NameIndexValueSchema, int_type, name='index')
node(NameIndexValueSchema, value_type, name='value')


NameWhereRefValueValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameWhereRefValueValueSchema, name_ref_type, name='name')
node(NameWhereRefValueValueSchema, lark_string, name='where')
node(NameWhereRefValueValueSchema, value_type, name='refvalue')
node(NameWhereRefValueValueSchema, value_type, name='value')


SortSchema = LarkSchemaNode(LarkMappingSchema())
node(SortSchema, name_ref_type, name='name')
node(SortSchema, lark_string, name='start', missing=None)
node(SortSchema, int_type, name='num', missing=None)
node(SortSchema, name_ref_type, name='by', missing=None)
SortSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(name_ref_type), name='get', accept_scalar=True, missing=None))
node(SortSchema, string_bool, name='desc', missing=False)
node(SortSchema, string_bool, name='alpha', missing=False)
node(SortSchema, name_ref_type, name='store', missing=None)
node(SortSchema, string_bool, name='groups', missing=False)


CursorMatchCountSchema = LarkSchemaNode(LarkMappingSchema())
node(CursorMatchCountSchema, int_type, name='cursor')
node(CursorMatchCountSchema, name_ref_type, name='match')
node(CursorMatchCountSchema, int_type, name='count')


NameCursorMatchCountSchema = LarkSchemaNode(LarkMappingSchema())
node(NameCursorMatchCountSchema, name_ref_type, name='name')
node(NameCursorMatchCountSchema, int_type, name='cursor')
node(NameCursorMatchCountSchema, lark_string, name='match')
node(NameCursorMatchCountSchema, int_type, name='count')


BitOpSchema = LarkSchemaNode(LarkMappingSchema())
node(BitOpSchema, lark_string, name='operation')
node(BitOpSchema, name_ref_type, name='destkey')
BitOpSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(name_ref_type), name='key'))


NameTtlValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameTtlValueSchema, name_ref_type, name='name')
node(NameTtlValueSchema, int_type, name='ttl')
node(NameTtlValueSchema, value_type, name='key')


NameNumberSchema = LarkSchemaNode(LarkMappingSchema())
node(NameNumberSchema, name_ref_type, name='name')
node(NameNumberSchema, lark_string, name='number', missing=None)


NameMinMaxSchema = LarkSchemaNode(LarkMappingSchema())
node(NameMinMaxSchema, name_ref_type, name='name')
node(NameMinMaxSchema, lark_string, name='min')
node(NameMinMaxSchema, lark_string, name='max')


NameValueAmount = LarkSchemaNode(LarkMappingSchema())
node(NameValueAmount, name_ref_type, name='name')
node(NameValueAmount, value_type, name='value')
node(NameValueAmount, int_type, name='amount', missing=1)


NameKeySchema = LarkSchemaNode(LarkMappingSchema())
node(NameKeySchema, name_ref_type, name='name')
node(NameKeySchema, lark_string, name='key')


class NameKeysSchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        name = cstruct['name']
        keys = cstruct['key']
        return ([name] + keys, {})


NameKeysSchema = NameKeysSchemaNode(LarkMappingSchema())
node(NameKeysSchema, name_ref_type, name='name')
NameKeysSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(lark_string), name='key'))


class DestKeysSchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        dest = cstruct['dest']
        keys = cstruct['keys']
        return ([dest, keys], {})


DestKeysSchema = DestKeysSchemaNode(LarkMappingSchema())
node(DestKeysSchema, name_ref_type, name='dest')
DestKeysSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(lark_string), name='keys'))


class OperationDestKeysSchemaNode(LarkSchemaNode):

    def signature_from_cstruct(self, cstruct, redis_args, redis_kwargs):
        operation = cstruct['operation']
        dest = cstruct['dest']
        keys = cstruct['keys']
        return ([operation, dest] + keys, {})


OperationDestKeysSchema = OperationDestKeysSchemaNode(LarkMappingSchema())
node(OperationDestKeysSchema, name_ref_type, name='operation')
node(OperationDestKeysSchema, name_ref_type, name='dest')
OperationDestKeysSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(lark_string), name='keys'))


NameWeightTupleSchema = colander.SchemaNode(colander.Tuple())
NameWeightTupleSchema.add(colander.SchemaNode(lark_string, name='name'))
NameWeightTupleSchema.add(colander.SchemaNode(int_type, name='weight', missing=None))


class DestKeysAggregateSchemaNode(LarkSchemaNode):

    def from_request(self, args=None, kwargs=None, query_dict=None, request_json=None, redis_prefix=None):
        keys = request_json.get('keys')
        format = 'dict'
        if keys and isinstance(keys, dict):
            request_json['keys'] = keys.items()
        if keys and isinstance(keys, list):
            format = 'list'
            request_json['keys'] = [[x, None] for x in keys]

        cstruct = request_json

        self.redis_prefix = redis_prefix
        data = self.deserialize(cstruct)
        args, kwargs = self.signature_from_cstruct(data, format)

        return (args, kwargs)

    def signature_from_cstruct(self, cstruct, format):
        name = cstruct.get('dest')
        keys = cstruct.get('keys')
        if keys and format == 'dict':
            keys = dict(keys)

        if keys and format == 'list':
            keys = [x[0] for x in keys]

        aggregate = cstruct.get('aggregate')

        return ([name, keys], {'aggregate': aggregate})


DestKeysAggregateSchema = DestKeysAggregateSchemaNode(LarkMappingSchema())
node(DestKeysAggregateSchema, name_ref_type, name='dest')
DestKeysAggregateSchema.add(LarkSchemaNode(colander.Sequence(), NameWeightTupleSchema, name='keys'))
node(DestKeysAggregateSchema, lark_string, name='aggregate', missing=None)


KeyValueTupleSchema = colander.SchemaNode(colander.Tuple())
KeyValueTupleSchema.add(colander.SchemaNode(lark_string, name='key'))
KeyValueTupleSchema.add(colander.SchemaNode(value_type, name='value'))


class NameMappingSchemaNode(LarkSchemaNode):

    def from_request(self, args=None, kwargs=None, query_dict=None, request_json=None, redis_prefix=None):
        request_json = request_json if request_json else {}

        mapping = request_json.get('mapping')
        if mapping and isinstance(mapping, dict):
            request_json['mapping'] = mapping.items()

        cstruct = dict(zip(['name'], args))
        if kwargs:
            cstruct.update(kwargs)

        cstruct.update(request_json)

        self.redis_prefix = redis_prefix
        data = self.deserialize(cstruct)
        args, kwargs = self.signature_from_cstruct(data, format)

        return (args, kwargs)

    def signature_from_cstruct(self, cstruct, format):
        name = cstruct.get('name')
        mapping = cstruct.get('mapping')
        if mapping:
            mapping = dict(mapping)

        return ([name, mapping], {})


NameMapingSchema = NameMappingSchemaNode(LarkMappingSchema())
node(NameMapingSchema, name_ref_type, name='name')
NameMapingSchema.add(LarkSchemaNode(colander.Sequence(), NameWeightTupleSchema, name='mapping'))


class NameKeyListSchemaNode(LarkSchemaNode):
    def signature_from_cstruct(self, cstruct, redis_keys, redis_args):
        name = cstruct.get('name')
        keys = cstruct.get('key')

        return ([name, keys], {})

NameKeyListSchema = NameKeyListSchemaNode(LarkMappingSchema())
node(NameKeyListSchema, name_ref_type, name='name')
NameKeyListSchema.add(LarkSchemaNode(colander.Sequence(), LarkSchemaNode(lark_string), name='key'))

ScanSchema = LarkSchemaNode(LarkMappingSchema())
node(ScanSchema, name_ref_type, name='match', missing=None)
node(ScanSchema, int_type, name='cursor', missing=0)
node(ScanSchema, int_type, name='count', missing=None)


NameScanSchema = LarkSchemaNode(LarkMappingSchema())
node(NameScanSchema, name_ref_type, name='name')
node(NameScanSchema, name_ref_type, name='match', missing=None)
node(NameScanSchema, int_type, name='cursor', missing=0)
node(NameScanSchema, int_type, name='count', missing=None)


NameKeyValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameKeyValueSchema, name_ref_type, name='name')
node(NameKeyValueSchema, lark_string, name='key')
node(NameKeyValueSchema, value_type, name='value')


NameKeyAmountSchema = LarkSchemaNode(LarkMappingSchema())
node(NameKeyAmountSchema, name_ref_type, name='name')
node(NameKeyAmountSchema, lark_string, name='key')
node(NameKeyAmountSchema, int_type, name='amount', missing=1)


NameKeyFloatAmountSchema = LarkSchemaNode(LarkMappingSchema())
node(NameKeyFloatAmountSchema, name_ref_type, name='name')
node(NameKeyFloatAmountSchema, lark_string, name='key')
node(NameKeyFloatAmountSchema, float_type, name='amount', missing=1.0)


valid_cast_funcs = {
    'int': int,
    'str': str,
    'float': float,
}


class ZrangeByScoresSchemaNode(LarkSchemaNode):
    def signature_from_cstruct(self, cstruct, redis_keys, redis_args):
        name = cstruct.get('name')
        min = cstruct.get('min')
        max = cstruct.get('max')
        start = cstruct.get('start')
        num = cstruct.get('num')
        withscores = cstruct.get('withscores')
        score_cast_func = valid_cast_funcs.get(cstruct.get('score_cast_func'))
        # print 'Sendcing up score_cast_func: %s %s' % (score_cast_func, type(score_cast_func))
        return ([name, min, max], {
            'start': start,
            'num': num,
            'withscores': withscores,
            'score_cast_func': score_cast_func,
        })


ZrangeByScoresSchema = ZrangeByScoresSchemaNode(LarkMappingSchema())
node(ZrangeByScoresSchema, name_ref_type, name='name')
node(ZrangeByScoresSchema, int_type, name='min')
node(ZrangeByScoresSchema, int_type, name='max')
node(ZrangeByScoresSchema, int_type, name='start', missing=None)
node(ZrangeByScoresSchema, int_type, name='num', missing=None)
node(ZrangeByScoresSchema, string_bool, name='withscores', missing=False)
node(ZrangeByScoresSchema, lark_string, name='score_cast_func', missing='float')


class ZrevRangeSchemaNode(LarkSchemaNode):
    def signature_from_cstruct(self, cstruct, redis_keys, redis_args):
        name = cstruct.get('name')
        start = cstruct.get('start')
        end = cstruct.get('end')
        withscores = cstruct.get('withscores')
        score_cast_func = valid_cast_funcs.get(cstruct.get('score_cast_func'))
        return ([name, start, end], {
            'withscores': withscores,
            'score_cast_func': score_cast_func,
        })


ZrevRangeSchema = ZrevRangeSchemaNode(LarkMappingSchema())
node(ZrevRangeSchema, name_ref_type, name='name')
node(ZrevRangeSchema, int_type, name='start')
node(ZrevRangeSchema, int_type, name='end')
node(ZrevRangeSchema, string_bool, name='withscores', missing=False)
node(ZrevRangeSchema, lark_string, name='score_cast_func', missing='float')


class ZrangeSchemaNode(LarkSchemaNode):
    def signature_from_cstruct(self, cstruct, redis_keys, redis_args):
        name = cstruct.get('name')
        start = cstruct.get('start')
        end = cstruct.get('end')
        desc = cstruct.get('desc')
        withscores = cstruct.get('withscores')
        score_cast_func = valid_cast_funcs.get(cstruct.get('score_cast_func'))
        return ([name, start, end], {
            'desc': desc,
            'withscores': withscores,
            'score_cast_func': score_cast_func,
        })


ZrangeSchema = ZrangeSchemaNode(LarkMappingSchema())
node(ZrangeSchema, name_ref_type, name='name')
node(ZrangeSchema, int_type, name='start')
node(ZrangeSchema, int_type, name='end')
node(ZrangeSchema, string_bool, name='desc', missing=False)
node(ZrangeSchema, string_bool, name='withscores', missing=False)
node(ZrangeSchema, lark_string, name='score_cast_func', missing='float')


NameTtlBinValueSchema = LarkSchemaNode(LarkMappingSchema())
node(NameTtlBinValueSchema, name_ref_type, name='name')
node(NameTtlBinValueSchema, int_type, name='ttl')
node(NameTtlBinValueSchema, bin_type, name='value')
