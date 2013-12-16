from colander import Invalid
from lark.redis import schemas
import unittest


"""Unit tests"""
class SchemaTests(unittest.TestCase):

    def run_schema(self, schema, cstruct):
        # schema = schema_cls()
        schema.redis_prefix = 'awesome'
        return schema.deserialize(cstruct)

    def test_key_schema(self):
        cstruct = {'key': 'awesome'}
        self.run_schema(schemas.KeySchema, cstruct)
        cstruct = {}
        with self.assertRaises(Invalid):
            data = self.run_schema(schemas.KeySchema, cstruct)
            print data

    def test_value_schema(self):
        cstruct = {'value': 'awesome'}
        self.run_schema(schemas.ValueSchema, cstruct)

    def test_key_value_schema(self):
        cstruct = {'key': 'awesome', 'value': 'awesome'}
        self.run_schema(schemas.KeyValueSchema, cstruct)

        data = {'key': 'a', 'value': 'value'}
        schemas.KeyValueSchema.redis_prefix = 'awesome'
        to_redis = schemas.KeyValueSchema.deserialize(data)
        self.assertEqual(to_redis['key'], 'awesome:a')

    def test_set_schema(self):
        cstruct = {'key': 'awesome', 'value': 'awesome'}
        self.run_schema(schemas.SetSchema, cstruct)

        cstruct['px'] = 1000
        self.run_schema(schemas.SetSchema, cstruct)

        cstruct['nx'] = True
        self.run_schema(schemas.SetSchema, cstruct)

        cstruct['nx'] = 1
        self.run_schema(schemas.SetSchema, cstruct)

    def test_bit_op_schema(self):
        cstruct = {'operation': 'awesome', 'destkey': 'cool', 'key': ['blah']}
        self.run_schema(schemas.BitOpSchema, cstruct)

        cstruct = {'operation': 'awesome', 'destkey': 'cool', 'key': 'blah'}
        with self.assertRaises(Invalid):
            self.run_schema(schemas.BitOpSchema, cstruct)

    def test_redis_reference_type(self):
        node = DummySchemaNode(None)
        node.redis_prefix = 'awesome'
        typ = schemas.PrefixedRedisReferenceType()
        result = typ.deserialize(node, 'test')
        self.assertEqual(result, 'awesome:test')
        result = typ.serialize(node, 'awesome:test')
        self.assertEqual(result, 'test')

    def test_lark_string_type(self):
        node = DummySchemaNode(None)
        typ = schemas.LarkString()
        # Normal strings
        result = typ.deserialize(node, 'test')
        self.assertEqual(result, 'test')
        # Empty strings
        result = typ.deserialize(node, '')
        self.assertEqual(result, '')

        # Even strings that look like numers
        result = typ.deserialize(node, '1')
        self.assertEqual(result, '1')

        # Integers can be strings too
        result = typ.deserialize(node, 1.0)
        self.assertEqual(result, '1.0') 

        # Integers can be strings too
        result = typ.deserialize(node, 1)
        self.assertEqual(result, '1')  


    def test_redis_value_type(self):
        node = DummySchemaNode(None)
        typ = schemas.RedisValueType()
        # Normal strings
        result = typ.deserialize(node, 'test')
        self.assertEqual(result, 'test')
        result = typ.serialize(node, result)
        self.assertEqual(result, 'test')

        # Empty strings
        result = typ.deserialize(node, '')
        self.assertEqual(result, '')
        result = typ.serialize(node, result)
        self.assertEqual(result, '')

        # Even strings that look like numers
        result = typ.deserialize(node, '1')
        self.assertEqual(result, '1')
        result = typ.serialize(node, result)
        self.assertEqual(result, '1')

        # Integers can be strings too
        result = typ.deserialize(node, 1)
        self.assertEqual(result, 1) 
        result = typ.serialize(node, result)
        self.assertEqual(result, 1)

        # Floats can be strings too
        result = typ.deserialize(node, 1.0)
        self.assertEqual(result, 1.0) 
        result = typ.serialize(node, result)
        self.assertEqual(result, 1.0)

        h = {'a': 'b'}
        result = typ.deserialize(node, h)
        self.assertEqual(result, '{"a": "b"}')
        result = typ.serialize(node, result)
        self.assertEqual(result, h)


class DummySchemaNode(object):
    def __init__(self, typ, name='', exc=None, default=None):
        self.typ = typ
        self.name = name
        self.exc = exc
        self.required = default is None
        self.default = default
        self.children = []

    def deserialize(self, val):
        from colander import Invalid
        if self.exc:
            raise Invalid(self, self.exc)
        return val

    def serialize(self, val):
        from colander import Invalid
        if self.exc:
            raise Invalid(self, self.exc)
        return val

    def __getitem__(self, name):
        for child in self.children:
            if child.name == name:
                return child

if __name__ == '__main__':
    unittest.main()