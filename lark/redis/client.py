from collections import namedtuple
import schemas


DEFAULT_INBOUND_SCHEMA = schemas.NoSchema
DEFAULT_OUTBOUND_SCHEMA = schemas.OutboundResultSchema


_RedisMethodDef = namedtuple('RedisMethodDef', 'inbound outbound')


class RedisMethodDef(_RedisMethodDef):

    @classmethod
    def from_kwargs(cls, inbound=DEFAULT_INBOUND_SCHEMA, outbound=DEFAULT_OUTBOUND_SCHEMA):
        return cls(inbound, outbound)


DEFAULT_SCHEMAS = RedisMethodDef(DEFAULT_INBOUND_SCHEMA, DEFAULT_OUTBOUND_SCHEMA)


class RedisApiClient(object):

    @classmethod
    def from_request(cls, redis_method, r, request_json, get_query_dict, url_args, url_kwargs):
        redis_api_client = cls()
        redis_args, redis_kwargs = redis_api_client.get_signature_from_request(redis_method, request_json, get_query_dict, url_args, url_kwargs)
        data = getattr(r, redis_method)(*redis_args, **redis_kwargs)
        response_data = redis_api_client.format_redis_response_for_http(redis_method, data)

        return response_data

    def get_signature_from_request(self, redis_method, request_json, get_query_dict, url_args, url_kwargs):
        # print 'args %s' % list(url_args)
        # print 'kwargs %s' % url_kwargs
        # print 'request.args %s' % get_query_dict
        # print 'request_json %s' % request_json

        InboundSchema = REDIST_METHOD_TO_SCHEMAS.get(redis_method, DEFAULT_SCHEMAS).inbound
        if not InboundSchema:
            InboundSchema = DEFAULT_INBOUND_SCHEMA

        args, kwargs = InboundSchema.from_request(url_args, url_kwargs, get_query_dict, request_json)
        return (args, kwargs)

    def format_redis_response_for_http(self, redis_method, data):
        OutboundSchema = REDIST_METHOD_TO_SCHEMAS.get(redis_method, DEFAULT_SCHEMAS).outbound
        if not OutboundSchema:
            OutboundSchema = DEFAULT_OUTBOUND_SCHEMA

        data = OutboundSchema.serialize(data)

        return data

no_args = ['bgrewriteaof', 'client_list', 'bgsave', 'client_getname', 'config_resetstat', 'dbsize', 'FLUSHALL', 'FLUSHDB', 'LASTSAVE',
           'ping', 'save', 'randomkey']

# build_api_func(OBJECT: NoSchema)
# def object(self, infotype, key):
#     "Return the encoding, idletime, or refcount about the key"
#     return self.execute_command('OBJECT', infotype, key, infotype=infotype)

REDIST_METHOD_TO_SCHEMAS = {
    'echo': RedisMethodDef.from_kwargs(schemas.ValueSchema),
    'client_kill': RedisMethodDef.from_kwargs(schemas.AddressSchema),
    'client_setname': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'config_get': RedisMethodDef.from_kwargs(schemas.PatternSchema),
    'config_set': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'debug_object': RedisMethodDef.from_kwargs(schemas.KeySchema),
    'info': RedisMethodDef.from_kwargs(schemas.SectionSchema),
    'get': RedisMethodDef.from_kwargs(schemas.KeySchema, schemas.OutboundValueSchema),
    'set': RedisMethodDef.from_kwargs(schemas.SetSchema),
    'append': RedisMethodDef.from_kwargs(schemas.KeyValueSchema),
    'setbit': RedisMethodDef.from_kwargs(schemas.NameOffsetBoolValueSchema),
    'bitcount': RedisMethodDef.from_kwargs(schemas.KeyRangeOptionalSchema),
    'bitop': RedisMethodDef.from_kwargs(schemas.OperationDestKeysSchema),
    'decr': RedisMethodDef.from_kwargs(schemas.NameAmountSchema),
    'delete': RedisMethodDef.from_kwargs(schemas.NamesSchema),
    'dump': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'restore': RedisMethodDef.from_kwargs(schemas.NameTtlValueSchema),
    'exists': RedisMethodDef.from_kwargs(schemas.KeySchema),
    'expire': RedisMethodDef.from_kwargs(schemas.NameTimeSchema),
    'expireat': RedisMethodDef.from_kwargs(schemas.NameWhenSchema),
    'ttl': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'pexpire': RedisMethodDef.from_kwargs(schemas.NameTimeSchema),
    'pexpireat': RedisMethodDef.from_kwargs(schemas.NameWhenSchema),
    'pttl': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'psetex': RedisMethodDef.from_kwargs(schemas.NameTimeMsValueSchema),
    'persist': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'getbit': RedisMethodDef.from_kwargs(schemas.NameOffsetSchema),
    'getrange': RedisMethodDef.from_kwargs(schemas.KeyRangeSchema),
    'getset': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'incr': RedisMethodDef.from_kwargs(schemas.NameAmountSchema, schemas.OutboundResultSchema),
    'incrbyfloat': RedisMethodDef.from_kwargs(schemas.NameFloatAmountSchema, schemas.OutboundResultSchema),
    'keys': RedisMethodDef.from_kwargs(schemas.PatternSchema),
    'mget': RedisMethodDef.from_kwargs(schemas.KeyListSchema),
    'mset': RedisMethodDef.from_kwargs(schemas.NameValueListSchema, schemas.OutboundValueSchema),
    'msetnx': RedisMethodDef.from_kwargs(schemas.NameValueListSchema, schemas.OutboundValueSchema),
    'rename': RedisMethodDef.from_kwargs(schemas.SrcDstSchema),
    'renamenx': RedisMethodDef.from_kwargs(schemas.SrcDstSchema),
    'setex': RedisMethodDef.from_kwargs(schemas.NameValueTimeSchema, schemas.OutboundValueSchema),
    'setnx': RedisMethodDef.from_kwargs(schemas.NameValueSchema, schemas.OutboundValueSchema),
    'setrange': RedisMethodDef.from_kwargs(schemas.NameOffsetStrValueSchema),
    'strlen': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'substr': RedisMethodDef.from_kwargs(schemas.NameRangeEndOptionalSchema, schemas.OutboundValueSchema),
    'type': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'blpop': RedisMethodDef.from_kwargs(schemas.KeysTimeoutSchema),
    'brpop': RedisMethodDef.from_kwargs(schemas.KeysTimeoutSchema),
    'brpoplpush': RedisMethodDef.from_kwargs(schemas.SrcDstTimeoutSchema),
    'lindex': RedisMethodDef.from_kwargs(schemas.NameIndexSchema),
    'linsert': RedisMethodDef.from_kwargs(schemas.NameWhereRefValueValueSchema),
    'llen': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'lpop': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'lpush': RedisMethodDef.from_kwargs(schemas.NameValuesSchema),
    'lpushx': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'lrange': RedisMethodDef.from_kwargs(schemas.NameRangeSchema),
    'lrem': RedisMethodDef.from_kwargs(schemas.NameNumValueSchema),
    'lset': RedisMethodDef.from_kwargs(schemas.NameIndexValueSchema),
    'ltrim': RedisMethodDef.from_kwargs(schemas.NameRangeSchema),
    'rpop': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'rpoplpush': RedisMethodDef.from_kwargs(schemas.SrcDstSchema),
    'rpush': RedisMethodDef.from_kwargs(schemas.NameValuesSchema),
    'rpushx': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'sort': RedisMethodDef.from_kwargs(schemas.SortSchema),
    'scan': RedisMethodDef.from_kwargs(schemas.ScanSchema),
    'sscan': RedisMethodDef.from_kwargs(schemas.NameScanSchema),
    'hscan': RedisMethodDef.from_kwargs(schemas.NameScanSchema),
    'zscan': RedisMethodDef.from_kwargs(schemas.NameScanSchema),
    'sadd': RedisMethodDef.from_kwargs(schemas.NameValuesSchema),
    'smembers': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'scard': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'sdiff': RedisMethodDef.from_kwargs(schemas.KeysSchema),
    'sdiffstore': RedisMethodDef.from_kwargs(schemas.DestKeysSchema),
    'sinter': RedisMethodDef.from_kwargs(schemas.KeysSchema),
    'sinterstore': RedisMethodDef.from_kwargs(schemas.DestKeysSchema),
    'sismember': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'smove': RedisMethodDef.from_kwargs(schemas.SrcDstValueSchema),
    'spop': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'srandmember': RedisMethodDef.from_kwargs(schemas.NameNumberSchema),
    'srem': RedisMethodDef.from_kwargs(schemas.RemNameValueListSchema),
    'sunion': RedisMethodDef.from_kwargs(schemas.KeysSchema),
    'sunionstore': RedisMethodDef.from_kwargs(schemas.DestKeysSchema),
    'zadd': RedisMethodDef.from_kwargs(schemas.NameScoreListSchema),
    'zcard': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'zcount': RedisMethodDef.from_kwargs(schemas.NameMinMaxSchema),
    'zincrby': RedisMethodDef.from_kwargs(schemas.NameValueAmount),
    'zinterstore': RedisMethodDef.from_kwargs(schemas.DestKeysAggregateSchema),
    'zrange': RedisMethodDef.from_kwargs(schemas.ZrangeSchema),
    'zrangebyscore': RedisMethodDef.from_kwargs(schemas.ZrangeByScoresSchema),
    'zrevrangebyscore': RedisMethodDef.from_kwargs(schemas.ZrangeByScoresSchema),
    'zrank': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'zrevrank': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'zrem': RedisMethodDef.from_kwargs(schemas.RemNameValueListSchema),
    'zremrangebyrank': RedisMethodDef.from_kwargs(schemas.NameMinMaxSchema),
    'zremrangebyscore': RedisMethodDef.from_kwargs(schemas.NameMinMaxSchema),
    'zrevrange': RedisMethodDef.from_kwargs(schemas.ZrevRangeSchema),
    'zscore': RedisMethodDef.from_kwargs(schemas.NameValueSchema),
    'zunionstore': RedisMethodDef.from_kwargs(schemas.DestKeysAggregateSchema),
    'hget': RedisMethodDef.from_kwargs(schemas.NameKeySchema),
    'hgetall': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'hexists': RedisMethodDef.from_kwargs(schemas.NameKeySchema),
    'hdel': RedisMethodDef.from_kwargs(schemas.NameKeysSchema),
    'hincrby': RedisMethodDef.from_kwargs(schemas.NameKeyAmountSchema),
    'hincrbyfloat': RedisMethodDef.from_kwargs(schemas.NameKeyFloatAmountSchema),
    'hkeys': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'hlen': RedisMethodDef.from_kwargs(schemas.NameSchema),
    'hset': RedisMethodDef.from_kwargs(schemas.NameKeyValueSchema),
    'hsetnx': RedisMethodDef.from_kwargs(schemas.NameKeyValueSchema),
    'hmset': RedisMethodDef.from_kwargs(schemas.NameMapingSchema),
    'hmget': RedisMethodDef.from_kwargs(schemas.NameKeyListSchema),
    'hvals': RedisMethodDef.from_kwargs(schemas.NameSchema),
}
