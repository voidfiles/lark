from __future__ import with_statement
import binascii
import datetime
import json
import time
import unittest
from urllib import urlencode

from flask import Flask
from iso8601 import parse_date
from redis._compat import b

from lark.ext.flask.redis_api import redis_api_blueprint 
from lark.ext.flask.flask_redis import Redis

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost:6379/10'
app.config['DEBUG'] = True
app.config['DEFAULT_LARK_SCOPES'] = set(['admin'])
Redis(app)
app.register_blueprint(redis_api_blueprint, url_prefix='/api/0')


class TestRedisCommands(unittest.TestCase):

    def setUp(self):
        self.app_ref = app
        self.app = app.test_client()

    def tearDown(self):
        self.api_request('/FLUSHDB/', method='DELETE')

    def api_request(self, path, method='GET', params=None, data=None, headers=None, assert_status_code=200, error_string=None, content_type='application/json'):
        data = json.dumps(data) if data else None

        query_string = None
        if params:
            query_string = urlencode(params)

        resp = self.app.open('/api/0%s' % path, method=method, query_string=query_string, data=data,
                                headers=headers, content_type='application/json')
        print resp.data
        if assert_status_code:
            self.assertEquals(assert_status_code, resp.status_code)

        resp = json.loads(resp.data)
        if error_string:
            self.assertEquals(resp['meta']['error_message'], error_string)

        return (resp.get('meta'), resp.get('data'))

    def arp(self, path, data=None):
        _, data = self.api_request(path, method='POST', data=data)
        return data

    def ard(self, path, params=None):
        _, data = self.api_request(path, method='DELETE', params=params)
        return data

    def arg(self, path, params=None, assert_status_code=200, error_string=None):
        _, data = self.api_request(path, params=params, assert_status_code=assert_status_code, error_string=error_string, content_type=None)
        return data

    ### SERVER INFORMATION ###
    def test_scope_getter(self):
        DEFAULT_LARK_SCOPES = self.app_ref.config['DEFAULT_LARK_SCOPES']
        self.app_ref.config['DEFAULT_LARK_SCOPES'] = None

        def scope_getter(*args, **kwargs):
            return set(['admin'])

        self.app_ref.config['LARK_SCOPE_GETTER'] = scope_getter

        meta, data = self.api_request('/CLIENT/LIST/')
        assert isinstance(data[0], dict)
        assert 'addr' in data[0]

        self.app_ref.config['DEFAULT_LARK_SCOPES'] = DEFAULT_LARK_SCOPES
        self.app_ref.config['LARK_SCOPE_GETTER'] = None

    def test_client_list(self):
        meta, data = self.api_request('/CLIENT/LIST/')
        assert isinstance(data[0], dict)
        assert 'addr' in data[0]

    def test_config_get(self):
        meta, data = self.api_request('/CONFIG/GET/')
        assert 'maxmemory' in data
        assert data['maxmemory'].isdigit()

    def test_config_resetstat(self):
        self.api_request('/PING/')
        meta, info = self.api_request('/INFO/')
        assert int(info['total_commands_processed']) > 1
        meta, data = self.api_request('/CONFIG/RESETSTAT/', method='POST')
        meta, info = self.api_request('/INFO/')
        # There is an implicit select when you connect to db 10
        assert int(info['total_commands_processed']) == 2

    def test_config_set(self):
        meta, data = self.api_request('/CONFIG/GET/')
        maxclients = data['maxclients']
        try:
            meta, data = self.api_request('/CONFIG/SET/maxclients/', method='POST',
                                          data={'value': '9999'})
            meta, data = self.api_request('/CONFIG/GET/')
            assert data['maxclients'] == '9999'
        finally:
            meta, data = self.api_request('/CONFIG/SET/maxclients/', method='POST',
                                          data={'value': maxclients})

    def test_dbsize(self):
        self.api_request('/SET/a/', method='POST', data={'value': 'foo'})
        self.api_request('/SET/b/', method='POST', data={'value': 'bar'})
        meta, data = self.api_request('/DBSIZE/')
        assert data == 2

    # def test_debug_object(self):
    #     self.api_request('/SET/', method='POST', data={'key': 'a', 'value': 'foo'})
    #     debug_info = r.debug_object('a')
    #     assert len(debug_info) > 0
    #     assert 'refcount' in debug_info
    #     assert debug_info['refcount'] == 1

    def test_echo(self):
        _, data = self.api_request('/ECHO/', method='POST', data={'value': 'foo bar'})
        assert data == 'foo bar'

    def test_info(self):
        self.api_request('/SET/a/', method='POST', data={'value': 'foo'})
        self.api_request('/SET/b/', method='POST', data={'value': 'bar'})
        _, info = self.api_request('/INFO/')
        assert isinstance(info, dict)
        assert info['db10']['keys'] == 2

    def test_lastsave(self):
        _, data = self.api_request('/LASTSAVE/')
        lastsave = parse_date(data)
        assert isinstance(lastsave, datetime.datetime)

    # def test_object(self):
    #     self.api_request('/SET/', method='POST', data={'key': 'a', 'value': 'foo'})
    #     _, data = self.api_request('/OBJECT/refcount/a')
    #     assert isinstance(data, int)
    #     _, data = self.api_request('/OBJECT/idlecount/a')
    #     assert isinstance(data, int)
    #     _, data = self.api_request('/OBJECT/encoding/a')
    #     assert data == 'raw'

    def test_ping(self):
        self.api_request('/PING/')

    ### BASIC KEY COMMANDS ###
    def test_append(self):
        data = self.arp('/APPEND/a/', {'value': 'a1'})
        assert data == 2
        data = self.arg('/GET/a/')
        assert data == 'a1'
        data = self.arp('/APPEND/a/', {'value': 'a2'})
        assert data == 4
        data = self.arg('/GET/a/')
        assert data == 'a1a2'

    def test_bitcount(self):
        self.arp('/SETBIT/a/', data={'offset': 5, 'value': True})
        assert self.arg('/BITCOUNT/a/') == 1
        self.arp('/SETBIT/a/', data={'offset': 6, 'value': True})
        assert self.arg('/BITCOUNT/a/') == 2
        self.arp('/SETBIT/a/', data={'offset': 5, 'value': False})
        assert self.arg('/BITCOUNT/a/') == 1
        self.arp('/SETBIT/a/', data={'offset': 9, 'value': True})
        self.arp('/SETBIT/a/', data={'offset': 17, 'value': True})
        self.arp('/SETBIT/a/', data={'offset': 25, 'value': True})
        self.arp('/SETBIT/a/', data={'offset': 33, 'value': True})
        assert self.arg('/BITCOUNT/a/') == 5
        assert self.arg('/BITCOUNT/a/0/-1/') == 5
        assert self.arg('/BITCOUNT/a/2/3/') == 2
        assert self.arg('/BITCOUNT/a/2/-1/') == 3
        assert self.arg('/BITCOUNT/a/-2/-1/') == 2
        assert self.arg('/BITCOUNT/a/1/1/') == 1

    # def test_bitop_not_empty_string(self):
    #     self.arp('/SET/', {'key': 'a', 'value': ''})
    #     self.arp('/BITOP/', {'operation': 'not', 'dest': 'r', 'keys': ['a']})
    #     assert self.arg('/GET/r/') is None

    # def test_bitop_not(self):
    #     test_str = b(u'\xAA\x00\xFF\x55')
    #     correct = ~0xAA00FF55 & 0xFFFFFFFF
    #     self.arp('/SET/', {'key': 'a', 'value': test_str})
    #     self.arp('/BITOP/', {'operation': 'not', 'dest': 'r', 'keys': ['a']})
    #     assert int(binascii.hexlify(self.arg('/GET/r/')), 16) == correct

    # def test_bitop_not_in_place(self):
    #     test_str = b(u'\xAA\x00\xFF\x55')
    #     correct = ~0xAA00FF55 & 0xFFFFFFFF
    #     self.arp('/SET/', {'key': 'a', 'value': test_str})
    #     self.arp('/BITOP/', {'operation': 'not', 'dest': 'a', 'keys': ['a']})
    #     assert int(binascii.hexlify(self.arg('/GET/r/')), 16) == correct

    # def test_bitop_single_string(self):
    #     test_str = b(u'\x01\x02\xFF')
    #     self.arp('/SET/', {'key': 'a', 'value': test_str})
    #     self.arp('/BITOP/', {'operation': 'and', 'dest': 'res1', 'keys': ['a']})
    #     self.arp('/BITOP/', {'operation': 'or', 'dest': 'res2', 'keys': ['a']})
    #     self.arp('/BITOP/', {'operation': 'xor', 'dest': 'res3', 'keys': ['a']})
    #     assert self.arg('/GET/res1/') == test_str
    #     assert self.arg('/GET/res2/') == test_str
    #     assert self.arg('/GET/res3/') == test_str

    # def test_bitop_string_operands(self):
    #     self.arp('/SET/', {'key': 'a', 'value': b('\x01\x02\xFF\xFF')})
    #     self.arp('/SET/', {'key': 'b', 'value': b('\x01\x02\xFF')})
    #     self.arp('/BITOP/', {'operation': 'and', 'dest': 'res1', 'keys': ['a', 'b']})
    #     self.arp('/BITOP/', {'operation': 'or', 'dest': 'res2', 'keys': ['a', 'b']})
    #     self.arp('/BITOP/', {'operation': 'xor', 'dest': 'res3', 'keys': ['a', 'b']})
    #     assert int(binascii.hexlify(self.arg('/GET/res1/')), 16) == 0x0102FF00
    #     assert int(binascii.hexlify(self.arg('/GET/res2/')), 16) == 0x0102FFFF
    #     assert int(binascii.hexlify(self.arg('/GET/res3/')), 16) == 0x000000FF

    def test_decr(self):
        self.arp('/DECR/a/')
        data = self.arg('/GET/a/')
        assert data == '-1'
        data = self.arp('/DECR/a/')
        assert data == -2
        data = self.arg('/GET/a/')
        assert data == '-2'
        data = self.arp('/DECRBY/a/', data={'amount': '5'})
        assert data == -7
        data = self.arg('/GET/a/')
        assert data == b('-7')

    def test_delete(self):
        data = self.ard('/DEL/a/')
        assert data == 0
        self.arp('/SET/a/', {'value': 'foo'})
        data = self.ard('/DEL/a/')
        assert data == 1

    def test_delete_with_multiple_keys(self):
        self.arp('/SET/a/', {'value': 'foo'})
        self.arp('/SET/b/', {'value': 'bar'})
        self.ard('/DEL/', params=[('name', 'a'), ('name', 'b')])
        assert self.arg('/GET/a/') is None
        assert self.arg('/GET/b/') is None

    # def test_dump_and_restore(self):
    #     self.arp('/SET/', {'key': 'a', 'value': 'foo'})
    #     dumped = self.arg('/DUMP/a/')
    #     self.ard('/DEL/a/')
    #     self.arp('/RESTORE/', {'name': 'a', 'ttl': 0, 'value': dumped})
    #     assert self.arg('/GET/a/') == b('foo')

    def test_exists(self):
        data = self.arg('/EXISTS/a/')
        assert not data
        data = self.arp('/SET/a/', {'value': 'foo'})
        assert data

    def test_expire(self):
        data = self.arp('/EXPIRE/a/', {'time': 10})
        assert not data
        self.arp('/SET/a/', {'value': 'foo'})
        data = self.arp('/EXPIRE/a/', {'time': 10})
        assert data
        data = self.arg('/TTL/a/')
        assert 0 < data <= 10
        data = self.arp('/PERSIST/a/')
        assert data
        data = self.arg('/TTL/a/')
        assert not data

    def test_expireat_datetime(self):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.arp('/SET/a/', {'value': 'foo'})
        self.arp('/EXPIREAT/a/', {'when': expire_at.isoformat()})
        data = self.arg('/TTL/a/')
        assert 0 < data <= 60

    def test_expireat_no_key(self):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        data = self.arp('/EXPIREAT/a/', {'when': expire_at.isoformat()})
        assert not data

    def test_get_and_set(self):
        # get and set can't be tested independently of each other
        _, data = self.api_request('/GET/a/')
        assert data is None
        byte_string = b('value')
        integer = 5
        self.arp('/SET/byte_string/', {'value': byte_string})
        self.arp('/SET/integer/', {'value': '5'})
        _, data = self.api_request('/GET/byte_string/')
        assert data == byte_string
        _, data = self.api_request('/GET/integer/')
        assert data == b(str(integer))

    def test_get_set_bit(self):
        # no value
        _, data = self.api_request('/GETBIT/a/5/')
        assert not data
        # set bit 5
        self.api_request('/SETBIT/a/', method='POST', data={'offset': 5, 'value': True})
        _, data = self.api_request('/GETBIT/a/5/')
        # unset bit 4
        _, data = self.api_request('/SETBIT/a/', method='POST', data={'offset': 4, 'value': False})
        assert not data
        _, data = self.api_request('/GETBIT/a/4/')
        assert not data
        # set bit 4
        _, data = self.api_request('/SETBIT/a/', method='POST', data={'offset': 4, 'value': True})
        assert not data
        _, data = self.api_request('/GETBIT/a/4/')
        assert data
        # set bit 5 again
        _, data = self.api_request('/SETBIT/a/', method='POST', data={'offset': 5, 'value': True})
        assert data
        _, data = self.api_request('/GETBIT/a/5/')
        assert data

    def test_getrange(self):
        self.api_request('/SET/a/', method='POST', data={'value': 'foo'})
        data = self.arg('/GETRANGE/a/0/0/')
        assert data == b('f')
        data = self.arg('/GETRANGE/a/0/2/')
        assert data == b('foo')
        data = self.arg('/GETRANGE/a/3/4/')
        assert data == b('')

    def test_getset(self):
        _, data = self.api_request('/GETSET/a/', method='POST', data={'value': 'foo'})
        assert data is None
        _, data = self.api_request('/GETSET/a/', method='POST', data={'value': 'bar'})
        assert data == b('foo')

    def test_incr(self):
        self.arp('/INCR/a/')
        data = self.arg('/GET/a/')
        assert data == '1'
        data = self.arp('/INCR/a/')
        assert data == 2
        data = self.arg('/GET/a/')
        assert data == '2'
        data = self.arp('/INCRBY/a/', {'amount': '5'})
        assert data == 7
        data = self.arg('/GET/a/')
        assert data == b('7')

    def test_incrby(self):
        data = self.arp('/INCRBY/a/')
        assert data == 1
        data = self.arp('/INCRBY/a/', {'amount': 4})
        assert data == 5
        data = self.arg('/GET/a/')
        assert data == b('5')

    def test_incrbyfloat(self):
        assert self.arp('/INCRBYFLOAT/a/') == 1.0
        assert self.arg('/GET/a/') == b('1')
        assert self.arp('/INCRBYFLOAT/a/', {'amount': 1.1})  == 2.1
        assert float(self.arg('/GET/a/')) == float(2.1)

    def test_keys(self):
        _, data = self.api_request('/KEYS/')
        assert data == []
        keys_with_underscores = set([b('test_a'), b('test_b')])
        keys = keys_with_underscores.union(set([b('testc')]))
        for key in keys:
            self.api_request('/SET/%s/' % key, method='POST', data={'value': '1'})
        _, data = self.api_request('/KEYS/test_*/')
        assert set(data) == keys_with_underscores
        _, data = self.api_request('/KEYS/test*/')
        assert set(data) == keys

    def test_mget(self):
        _, data = self.api_request('/MGET/', params=[('key', 'a'), ('key', 'b')])
        assert data == [None, None]
        self.api_request('/SET/a/', method='POST', data={'value': '1'})
        self.api_request('/SET/b/', method='POST', data={'value': '2'})
        self.api_request('/SET/c/', method='POST', data={'value': '3'})
        _, data = self.api_request('/MGET/', params=[('key', 'a'), ('key', 'other'), ('key', 'b'), ('key', 'c')])
        assert data == [b('1'), None, b('2'), b('3')]

    def test_mset(self):
        d = [('a', '1'), ('b', '2'), ('c', '3')]
        _, data = self.api_request('/MSET/', method='POST', data=d)
        assert data
        for k, v in d:
            _, data = self.api_request('/GET/%s/' % k)
            assert data == v

    def test_msetnx(self):
        d = [('a', '1'), ('b', '2'), ('c', '3')]
        _, data = self.api_request('/MSETNX/', method='POST', data=d)
        assert data
        d2 = [('a', 'x'), ('d', '4')]
        data = self.arp('/MSETNX/', d2)
        assert not data
        for k, v in d:
            data = self.arg('/GET/%s/' % k)
            assert data == v
        data = self.arg('/GET/d/')
        assert data is None

    def test_pexpire(self):
        assert not self.arp('/PEXPIRE/a/', {'time': 60000})
        self.arp('/SET/a/', {'value': 'foo'})
        assert self.arp('/PEXPIRE/a/', {'time': 60000})
        assert 0 < self.arg('/PTTL/a/') <= 60000
        assert self.arp('/PERSIST/a/')
        assert self.arg('/PTTL/a/') is None

    def test_pexpireat_no_key(self):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        assert not self.arp('/PEXPIREAT/a/', {'when': expire_at.isoformat()})

    def test_psetex(self):
        assert self.arp('/PSETEX/a/', {'time_ms': 1000, 'value': 'value'})
        assert self.arg('/GET/a/') == b('value')
        assert 0 < self.arg('/PTTL/a/') <= 1000

    def test_randomkey(self):
        _, data = self.api_request('/RANDOMKEY/')
        assert data is None
        for key in ('a', 'b', 'c'):
            self.api_request('/SET/%s/' % key, method='POST', data={'value': '1'})
        _, data = self.api_request('/RANDOMKEY/')
        assert data in (b('a'), b('b'), b('c'))

    def test_rename(self):
        self.api_request('/SET/a/', method='POST', data={'value': '1'})
        _, data = self.api_request('/RENAME/', method='POST', data={'src': 'a', 'dst': 'b'})
        assert data
        _, data = self.api_request('/GET/a/')
        assert data is None
        _, data = self.api_request('/GET/b/')
        assert data == b('1')

    def test_renamenx(self):
        self.arp('/SET/a/', {'value': '1'})
        self.arp('/SET/b/', {'value': '2'})
        _, data = self.api_request('/RENAMENX/', method='POST', data={'src': 'a', 'dst': 'b'})
        assert not data
        _, data = self.api_request('/GET/a/')
        assert data == b('1')
        _, data = self.api_request('/GET/b/')
        assert data == b('2')

    def test_set_nx(self):
        assert self.arp('/SET/a/', {'value': '1', 'nx': True})
        assert not self.arp('/SET/a/', {'value': '2', 'nx': True})
        assert self.arg('/GET/a/') == b('1')

    def test_set_xx(self):
        assert not self.arp('/SET/a/', {'value': '1', 'xx': True})
        assert self.arg('/GET/a/') is None
        self.arp('/SET/a/', {'value': 'bar'})
        assert self.arp('/SET/a/', {'value': '2', 'xx': True})
        assert self.arg('/GET/a/') == b('2')

    def test_set_px(self):
        assert self.arp('/SET/a/', {'value': '1', 'px': 10000})
        assert self.arg('/GET/a/') == b('1')
        assert 0 < self.arg('/PTTL/a/') <= 10000
        assert 0 < self.arg('/TTL/a/') <= 10

    def test_set_ex(self):
        assert self.arp('/SET/a/', {'value': '1', 'ex': 10})
        assert 0 < self.arg('/TTL/a/')  <= 10

    def test_set_multipleoptions(self):
        self.arp('/SET/a/', {'value': '1'})
        assert self.arp('/SET/a/', {'value': '1', 'xx': True, 'px': 10000})
        assert 0 < self.arg('/TTL/a/') <= 10

    def test_setex(self):
        _, data = self.api_request('/SETEX/a/', method='POST', data={'value': '1', 'time': 60})
        assert data
        _, data = self.api_request('/GET/a/')
        assert data == b('1')
        _, data = self.api_request('/TTL/a/')
        assert 0 < data <= 60

    def test_setnx(self):
        _, data = self.api_request('/SETNX/a/', method='POST', data={'value': '1'})
        assert data
        _, data = self.api_request('/GET/a/')
        assert data == b('1')
        _, data = self.api_request('/SETNX/a/', method='POST', data={'value': '2'})
        assert not data
        _, data = self.api_request('/GET/a/')
        assert data == '1'

    def test_setrange(self):
        _, data = self.api_request('/SETRANGE/a/', method='POST', data={'offset': 5, 'value': 'foo'})
        assert data == 8
        _, data = self.api_request('/GET/a/')
        assert data == b('\0\0\0\0\0foo')
        _, data = self.api_request('/SET/a/', method='POST', data={'value': 'abcdefghijh'})
        _, data = self.api_request('/SETRANGE/a/', method='POST', data={'offset': 6, 'value': '12345'})
        assert data
        _, data = self.api_request('/GET/a/')
        assert data == b('abcdef12345')

    def test_strlen(self):
        # String length is going to be weird because of the automatic JSON encoding
        self.api_request('/SET/a/', method='POST', data={'value': 'foo'})
        _, data = self.api_request('/STRLEN/a/')
        assert data == 3

    def test_substr(self):
        self.arp('/SET/a/', {'value': '0123456789'})
        _, data = self.api_request('/SUBSTR/a/0/')
        assert data == b('0123456789')
        _, data = self.api_request('/SUBSTR/a/2/')
        assert data == b('23456789')
        _, data = self.api_request('/SUBSTR/a/3/5/')
        assert data == b('345')
        _, data = self.api_request('/SUBSTR/a/3/-2/')
        assert data == b('345678')

    def test_type(self):
        assert self.arg('/TYPE/a/') == b('none')
        self.arp('/SET/a/', {'value': '1'})
        assert self.arg('/TYPE/a/') == b('string')
        self.ard('/DEL/a/')
        self.arp('/LPUSH/a/', {'values': ['1']})
        assert self.arg('/TYPE/a/') == b('list')
        self.ard('/DEL/a/')
        self.arp('/SADD/a/', data={'values': ['1']})
        assert self.arg('/TYPE/a/') == b('set')
        self.ard('/DEL/a/')
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/TYPE/a/') == b('zset')

    #### LIST COMMANDS ####
    #@unittest.skip('Include later')
    def test_blpop(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2']})
        self.api_request('/RPUSH/b/', method='POST', data={'values': ['3', '4']})
        _, data = self.api_request('/BLPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('b'), b('3')]
        _, data = self.api_request('/BLPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('b'), b('4')]
        _, data = self.api_request('/BLPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('a'), b('1')]
        _, data = self.api_request('/BLPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('a'), b('2')]
        _, data = self.api_request('/BLPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data is None
        self.api_request('/RPUSH/c/', method='POST', data={'values': ['1']})
        _, data = self.api_request('/BLPOP/', method='POST', data={'keys': ['c'], 'timeout': 1})
        assert data == [b('c'), b('1')]

    #@unittest.skip('Include later')
    def test_brpop(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2']})
        self.api_request('/RPUSH/b/', method='POST', data={'values': ['3', '4']})
        _, data = self.api_request('/BRPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('b'), b('4')]
        _, data = self.api_request('/BRPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('b'), b('3')]
        _, data = self.api_request('/BRPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('a'), b('2')]
        _, data = self.api_request('/BRPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data == [b('a'), b('1')]
        _, data = self.api_request('/BRPOP/', method='POST', data={'keys': ['b', 'a'], 'timeout': 1})
        assert data is None
        self.api_request('/RPUSH/c/', method='POST', data={'values': ['1']})
        _, data = self.api_request('/BRPOP/', method='POST', data={'keys': ['c'], 'timeout': 1})
        assert data == [b('c'), b('1')]

    #@unittest.skip('Include later')
    def test_brpoplpush(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2']})
        self.api_request('/RPUSH/b/', method='POST', data={'values': ['3', '4']})
        _, data = self.api_request('/BRPOPLPUSH/', method='POST', data={'src': 'a', 'dst': 'b'})
        assert data == b('2')
        _, data = self.api_request('/BRPOPLPUSH/', method='POST', data={'src': 'a', 'dst': 'b'})
        assert data == b('1')
        _, data = self.api_request('/BRPOPLPUSH/', method='POST', data={'src': 'a', 'dst': 'b', 'timeout': 1})
        assert data is None
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == []
        _, data = self.api_request('/LRANGE/b/0/-1/')
        assert data == [b('1'), b('2'), b('3'), b('4')]

    def test_brpoplpush_empty_string(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['']})
        _, data = self.api_request('/BRPOPLPUSH/', method='POST', data={'src': 'a', 'dst': 'b'})
        assert data == b('')

    def test_lindex(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3']})
        _, data = self.api_request('/LINDEX/a/0/')
        assert data == b('1')
        _, data = self.api_request('/LINDEX/a/1/')
        assert data == b('2')
        _, data = self.api_request('/LINDEX/a/2/')
        assert data == b('3')

    def test_linsert(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3']})
        _, data = self.api_request('/LINSERT/a/', method='POST', data={'where': 'after', 'refvalue': '2', 'value': '2.5'})
        assert data == 4
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == [b('1'), b('2'), b('2.5'), b('3')]
        _, data = self.api_request('/LINSERT/a/', method='POST', data={'where': 'before', 'refvalue': '2', 'value': '1.5'})
        assert data == 5
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == [b('1'), b('1.5'), b('2'), b('2.5'), b('3')]

    def test_llen(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3']})
        _, data = self.api_request('/LLEN/a/')
        assert data == 3

    def test_lpop(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3']})
        _, data = self.api_request('/LPOP/a/', method='POST')
        assert data == b('1')
        _, data = self.api_request('/LPOP/a/', method='POST')
        assert data == b('2')
        _, data = self.api_request('/LPOP/a/', method='POST')
        assert data == b('3')
        _, data = self.api_request('/LPOP/a/', method='POST')
        assert data is None

    def test_lpush(self):
        _, data = self.api_request('/LPUSH/a/', method='POST', data={'values': ['1']})
        assert data == 1
        _, data = self.api_request('/LPUSH/a/', method='POST', data={'values': ['2']})
        assert data == 2
        _, data = self.api_request('/LPUSH/a/', method='POST', data={'values': ['3', '4']})
        assert data == 4
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == [b('4'), b('3'), b('2'), b('1')]

    def test_lpushx(self):
        _, data = self.api_request('/LPUSHX/a/', method='POST', data={'value': '1'})
        assert data == 0
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == []
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3']})
        _, data = self.api_request('/LPUSHX/a/', method='POST', data={'value': '4'})
        assert data == 4
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == [b('4'), b('1'), b('2'), b('3')]

    def test_lrange(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3', '4', '5']})
        _, data = self.api_request('/LRANGE/a/0/2/')
        assert data == [b('1'), b('2'), b('3')]
        _, data = self.api_request('/LRANGE/a/2/10/')
        assert data == [b('3'), b('4'), b('5')]
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == [b('1'), b('2'), b('3'), b('4'), b('5')]

    def test_lrem(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '1', '1', '1']})
        _, data = self.api_request('/LREM/a/1/1/', method='DELETE')
        assert data == 1
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == [b('1'), b('1'), b('1')]
        _, data = self.api_request('/LREM/a/1/', method='DELETE')
        assert data == 3
        _, data = self.api_request('/LRANGE/a/0/-1/')
        assert data == []

    def test_lset(self):
        self.api_request('/RPUSH/a/', method='POST', data={'values': ['1', '2', '3']})
        assert self.arg('/LRANGE/a/0/-1/') == [b('1'), b('2'), b('3')]
        assert self.arp('/LSET/a/', data={'index': 1, 'value': '4'})
        assert self.arg('/LRANGE/a/0/2/') == [b('1'), b('4'), b('3')]

    def test_ltrim(self):
        self.arp('/RPUSH/a/', data={'values': ['1', '2', '3']})
        assert self.ard('/LTRIM/a/0/1/')
        assert self.arg('/LRANGE/a/0/-1/') == [b('1'), b('2')]

    def test_rpop(self):
        self.arp('/RPUSH/a/', data={'values': ['1', '2', '3']})
        assert self.arp('/RPOP/a/') == b('3')
        assert self.arp('/RPOP/a/') == b('2')
        assert self.arp('/RPOP/a/') == b('1')
        assert self.arp('/RPOP/a/') is None

    def test_rpoplpush(self):
        self.arp('/RPUSH/a/', data={'values': ['a1', 'a2', 'a3']})
        self.arp('/RPUSH/b/', data={'values': ['b1', 'b2', 'b3']})
        assert self.arp('/RPOPLPUSH/', data={'src': 'a', 'dst': 'b'}) == b('a3')
        assert self.arg('/LRANGE/a/0/-1/') == [b('a1'), b('a2')]
        assert self.arg('/LRANGE/b/0/-1/') == [b('a3'), b('b1'), b('b2'), b('b3')]

    def test_rpush(self):
        assert self.arp('/RPUSH/a/', data={'values': ['1']}) == 1
        assert self.arp('/RPUSH/a/', data={'values': ['2']}) == 2
        assert self.arp('/RPUSH/a/', data={'values': ['3', '4']}) == 4
        assert self.arg('/LRANGE/a/0/-1/') == [b('1'), b('2'), b('3'), b('4')]

    def test_rpushx(self):
        assert self.arp('/RPUSHX/a/', data={'value': 'b'}) == 0
        assert self.arg('/LRANGE/a/0/-1/') == []
        self.arp('/RPUSH/a/', data={'values': ['1', '2', '3']})
        assert self.arp('/RPUSHX/a/', data={'value': '4'}) == 4
        assert self.arg('/LRANGE/a/0/-1/') == [b('1'), b('2'), b('3'), b('4')]

    ### SCAN COMMANDS ###
    def test_scan(self):
        self.arp('/SET/a/', {'value': '1'})
        self.arp('/SET/b/', {'value': '2'})
        self.arp('/SET/c/', {'value': '3'})
        cursor, keys = self.arg('/SCAN/')
        assert cursor == b('0')
        assert set(keys) == set([b('a'), b('b'), b('c')])
        _, keys = self.arg('/SCAN/', params=[('match', 'a')])
        assert set(keys) == set([b('a')])

    def test_sscan(self):
        self.arp('/SADD/a/', data={'values': [1, 2, 3]})
        cursor, members = self.arg('/SSCAN/a/')
        assert cursor == b('0')
        assert set(members) == set([b('1'), b('2'), b('3')])
        _, members = self.arg('/SSCAN/a/', params=[('match', '1')])
        assert set(members) == set([b('1')])

    def test_hscan(self):
        self.arp('/HMSET/a/', {'mapping': {'a': 1, 'b': 2, 'c': 3}})
        cursor, dic = self.arg('/HSCAN/a/')
        assert cursor == b('0')
        assert dic == {b('a'): b('1'), b('b'): b('2'), b('c'): b('3')}
        _, dic = self.arg('/HSCAN/a/', params=[('match', 'a')])
        assert dic == {b('a'): b('1')}

    def test_zscan(self):
        self.arp('/ZADD/a/', {'scores': [('a', 1), ('b', 2), ('c', 3)]})
        cursor, pairs = self.arg('/ZSCAN/a/')
        assert cursor == b('0')
        assert pairs == [[b('a'), 1], [b('b'), 2], [b('c'), 3]]
        _, pairs = self.arg('/ZSCAN/a/', params=[('match', 'a')])
        assert pairs == [[b('a'), 1]]

    ### SET COMMANDS ###
    def test_sadd(self):
        members = [b('1'), b('2'), b('3')]
        self.arp('/SADD/a/', data={'values': members})
        assert set(self.arg('/SMEMBERS/a/')) == set(members)

    def test_scard(self):
        self.arp('/SADD/a/', data={'values': [b('1'), b('2'), b('3')]})
        assert self.arg('/SCARD/a/') == 3

    def test_sdiff(self):
        self.arp('/SADD/a/', data={'values': ['1', '2', '3']})
        params = [('key', 'a'), ('key', 'b')]
        assert set(self.arg('/SDIFF/', params=params)) == set([b('1'), b('2'), b('3')])
        self.arp('/SADD/b/', data={'values': ['2', '3']})
        assert set(self.arg('/SDIFF/', params=params)) == set([b('1')])

    def test_sdiffstore(self):
        members = ['1', '2', '3']
        self.arp('/SADD/a/', {'values': members})
        assert self.arp('/SDIFFSTORE/', {'dest': 'c', 'keys': ['a', 'b']}) == 3
        assert set(self.arg('/SMEMBERS/c/')) == set(members)
        self.arp('/SADD/b/', {'values': ['2', '3']})
        assert self.arp('/SDIFFSTORE/', {'dest': 'c', 'keys': ['a', 'b']}) == 1
        assert set(self.arg('/SMEMBERS/c/')) == set([b('1')])

    def test_sinter(self):
        self.arp('/SADD/a/', data={'values': ['1', '2', '3']})
        params = [('key', 'a'), ('key', 'b')]
        assert set(self.arg('/SINTER/', params=params)) == set([])
        self.arp('/SADD/b/', data={'values': ['2', '3']})
        assert set(self.arg('/SINTER/', params=params)) == set([b('2'), b('3')])

    def test_sinterstore(self):
        members = ['1', '2', '3']
        self.arp('/SADD/a/', {'values': members})
        assert self.arp('/SINTERSTORE/', {'dest': 'c', 'keys': ['a', 'b']}) == 0
        assert set(self.arg('/SMEMBERS/c/')) == set()
        self.arp('/SADD/b/', {'values': ['2', '3']})
        assert self.arp('/SINTERSTORE/', {'dest': 'c', 'keys': ['a', 'b']}) == 2
        assert set(self.arg('/SMEMBERS/c/')) == set([b('2'), b('3')])

    def test_sismember(self):
        self.arp('/SADD/a/', {'values': ['1', '2', '3']})
        assert self.arg('/SISMEMBER/a/1/')
        assert self.arg('/SISMEMBER/a/2/')
        assert self.arg('/SISMEMBER/a/3/')
        assert not self.arg('/SISMEMBER/a/4/')

    def test_smembers(self):
        self.arp('/SADD/a/', {'values': ['1', '2', '3']})
        assert set(self.arg('/SMEMBERS/a/')) == set([b('1'), b('2'), b('3')])

    def test_smove(self):
        self.arp('/SADD/a/', {'values': ['a1', 'a2']})
        self.arp('/SADD/b/', {'values': ['b1', 'b2']})
        assert self.arp('/SMOVE/', {'src': 'a', 'dst': 'b', 'value': 'a1'})
        assert set(self.arg('/SMEMBERS/a/')) == set([b('a2')])
        assert set(self.arg('/SMEMBERS/b/')) == set([b('b1'), b('b2'), b('a1')])

    def test_spop(self):
        s = [b('1'), b('2'), b('3')]
        self.arp('/SADD/a/', {'values': s})
        value = self.arp('/SPOP/a/')
        assert value in s
        assert set(self.arg('/SMEMBERS/a/')) == set(s) - set([value])

    def test_srandmember(self):
        s = [b('1'), b('2'), b('3')]
        self.arp('/SADD/a/', {'values': s})
        assert self.arg('/SRANDMEMBER/a/') in s

    def test_srandmember_multi_value(self):
        s = [b('1'), b('2'), b('3')]
        self.arp('/SADD/a/', {'values': s})
        randoms = self.arg('/SRANDMEMBER/a/2/')
        assert len(randoms) == 2
        assert set(randoms).intersection(s) == set(randoms)

    def test_srem(self):
        s = ['1', '2', '3', '4']
        self.arp('/SADD/a/', {'values': s})
        assert self.ard('/SREM/a/', params=[('value', '5')]) == 0
        assert self.ard('/SREM/a/', params=[('value', '2'), ('value', '4')]) == 2
        assert set(self.arg('/SMEMBERS/a/')) == set([b('1'), b('3')])

    def test_sunion(self):
        self.arp('/SADD/a/', {'values': ['1', '2']})
        self.arp('/SADD/b/', {'values': ['2', '3']})
        assert set(self.arg('/SUNION/', params=[('key', 'a'), ('key', 'b')])) == set([b('1'), b('2'), b('3')])

    def test_sunionstore(self):
        self.arp('/SADD/a/', {'values': ['1', '2']})
        self.arp('/SADD/b/', {'values': ['2', '3']})
        assert self.arp('/SUNIONSTORE/', {'dest': 'c', 'keys': ['a', 'b']}) == 3
        assert set(self.arg('/SMEMBERS/c/')) == set([b('1'), b('2'), b('3')])

    ### SORTED SET COMMANDS ###
    def test_zadd(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/ZRANGE/a/0/-1/') == [b('a1'), b('a2'), b('a3')]

    def test_zcard(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/ZCARD/a/') == 3

    def test_zcount(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/ZCOUNT/a/-inf/+inf/') == 3
        assert self.arg('/ZCOUNT/a/1/2/') == 2
        assert self.arg('/ZCOUNT/a/10/20/') == 0

    def test_zincrby(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})

        assert self.arp('/ZINCRBY/a/', {'value': 'a2'}) == 3.0
        assert self.arp('/ZINCRBY/a/', {'value': 'a3', 'amount': 5}) == 8.0
        assert self.arg('/ZSCORE/a/a2/') == 3.0
        assert self.arg('/ZSCORE/a/a3/') == 8.0

    def test_zinterstore_sum(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 1), ('a3', 1)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 2)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZINTERSTORE/', {'dest': 'd', 'keys': ['a', 'b', 'c']}) == 2
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == [[b('a3'), 8], [b('a1'), 9]]

    def test_zinterstore_max(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 1), ('a3', 1)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 2)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZINTERSTORE/', {'dest': 'd', 'keys': ['a', 'b', 'c'], 'aggregate': 'MAX'}) == 2
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == [[b('a3'), 5], [b('a1'), 6]]

    def test_zinterstore_min(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 3), ('a3', 5)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZINTERSTORE/', {'dest': 'd', 'keys': ['a', 'b', 'c'], 'aggregate': 'MIN'}) == 2
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == [[b('a1'), 1], [b('a3'), 3]]

    def test_zinterstore_with_weight(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 1), ('a3', 1)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 2)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZINTERSTORE/', {'dest': 'd', 'keys': {'a': 1, 'b': 2, 'c': 3},}) == 2
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == [[b('a3'), 20], [b('a1'), 23]]

    def test_zrange(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/ZRANGE/a/0/1/') == [b('a1'), b('a2')]
        assert self.arg('/ZRANGE/a/1/2/')  == [b('a2'), b('a3')]

        # withscores
        assert self.arg('/ZRANGE/a/0/1/', params=[('withscores', 1)]) == [[b('a1'), 1.0], [b('a2'), 2.0]]
        assert self.arg('/ZRANGE/a/1/2/', params=[('withscores', 1)]) == [[b('a2'), 2.0], [b('a3'), 3.0]]

        # custom score function
        assert self.arg('/ZRANGE/a/0/1/', params=[('withscores', 1), ('score_cast_func', 'int')]) == \
            [[b('a1'), 1], [b('a2'), 2]]

    def test_zrangebyscore(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3), ('a4', 4), ('a5', 5)]})
        assert self.arg('/ZRANGEBYSCORE/a/2/4/') == [b('a2'), b('a3'), b('a4')]

        # slicing with start/num
        assert self.arg('/ZRANGEBYSCORE/a/2/4/', params=[('start', 1), ('num', 2)]) == [b('a3'), b('a4')]

        # withscores
        assert self.arg('/ZRANGEBYSCORE/a/2/4/', params=[('withscores', 1)]) == \
            [[b('a2'), 2.0], [b('a3'), 3.0], [b('a4'), 4.0]]

        # custom score function
        assert self.arg('/ZRANGEBYSCORE/a/2/4/', params=[('withscores', 1), ('score_cast_func', 'int')]) == \
            [[b('a2'), 2], [b('a3'), 3], [b('a4'), 4]]

    def test_zrank(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3), ('a4', 4), ('a5', 5)]})
        assert self.arg('/ZRANK/a/a1/') == 0
        assert self.arg('/ZRANK/a/a2/') == 1
        assert self.arg('/ZRANK/a/a6/') == None

    def test_zrem(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.ard('/ZREM/a/', params=[('value', 'a2')]) == 1
        assert self.arg('/ZRANGE/a/0/-1/') == [b('a1'), b('a3')]
        assert self.ard('/ZREM/a/', params=[('value', 'b')]) == 0
        assert self.arg('/ZRANGE/a/0/-1/') == [b('a1'), b('a3')]

    def test_zrem_multiple_keys(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.ard('/ZREM/a/', params=[('value', 'a1'), ('value', 'a2')]) == 2
        assert self.arg('/ZRANGE/a/0/5/') == [b('a3')]

    def test_zremrangebyrank(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3), ('a4', 4), ('a5', 5)]})
        assert self.ard('/ZREMRANGEBYRANK/a/1/3/') == 3
        assert self.arg('/ZRANGE/a/0/5/') == [b('a1'), b('a5')]

    def test_zremrangebyscore(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3), ('a4', 4), ('a5', 5)]})
        assert self.ard('/ZREMRANGEBYSCORE/a/2/4/') == 3
        assert self.arg('/ZRANGE/a/0/-1/') == [b('a1'), b('a5')]
        assert self.ard('/ZREMRANGEBYSCORE/a/2/4/') == 0
        assert self.arg('/ZRANGE/a/0/-1/') == [b('a1'), b('a5')]

    def test_zrevrange(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/ZREVRANGE/a/0/1/') == [b('a3'), b('a2')]
        assert self.arg('/ZREVRANGE/a/1/2/') == [b('a2'), b('a1')]

        # withscores
        assert self.arg('/ZREVRANGE/a/0/1/', params=[('withscores', 1)]) == \
            [[b('a3'), 3.0], [b('a2'), 2.0]]
        assert self.arg('/ZREVRANGE/a/1/2/', params=[('withscores', 1)]) == \
            [[b('a2'), 2.0], [b('a1'), 1.0]]

        # custom score function
        assert self.arg('/ZREVRANGE/a/0/1/', params=[('withscores', 1), ('score_cast_func', 'int')]) == \
            [[b('a3'), 3], [b('a2'), 2]]

    def test_zrevrangebyscore(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3), ('a4', 4), ('a5', 5)]})
        assert self.arg('/ZREVRANGEBYSCORE/a/4/2/') == [b('a4'), b('a3'), b('a2')]

        # slicing with start/num
        assert self.arg('/ZREVRANGEBYSCORE/a/4/2/', params=[('start', 1), ('num', 2)]) == \
            [b('a3'), b('a2')]

        # withscores
        assert self.arg('/ZREVRANGEBYSCORE/a/4/2/', params=[('withscores', 1)]) == \
            [[b('a4'), 4.0], [b('a3'), 3.0], [b('a2'), 2.0]]

        # custom score function
        assert self.arg('/ZREVRANGEBYSCORE/a/4/2/', params=[('withscores', 1), ('score_cast_func', 'int')]) == \
            [[b('a4'), 4], [b('a3'), 3], [b('a2'), 2]]

    def test_zrevrank(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3), ('a4', 4), ('a5', 5)]})
        assert self.arg('/ZREVRANK/a/a1/') == 4
        assert self.arg('/ZREVRANK/a/a2/') == 3
        assert self.arg('/ZREVRANK/a/a6/') is None

    def test_zscore(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        assert self.arg('/ZSCORE/a/a1/') == 1.0
        assert self.arg('/ZSCORE/a/a2/') == 2.0
        assert self.arg('/ZSCORE/a/a4/') is None

    def test_zunionstore_sum(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 1), ('a3', 1)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 2)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZUNIONSTORE/', {'dest': 'd', 'keys': ['a', 'b', 'c']}) == 4
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == \
            [[b('a2'), 3], [b('a4'), 4], [b('a3'), 8], [b('a1'), 9]]

    def test_zunionstore_max(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 1), ('a3', 1)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 2)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZUNIONSTORE/', {'dest': 'd', 'keys': ['a', 'b', 'c'], 'aggregate': 'MAX'}) == 4
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == \
            [[b('a2'), 2], [b('a4'), 4], [b('a3'), 5], [b('a1'), 6]]

    def test_zunionstore_min(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 2), ('a3', 3)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 4)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZUNIONSTORE/', {'dest': 'd', 'keys': ['a', 'b', 'c'], 'aggregate': 'MIN'}) == 4
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == \
            [[b('a1'), 1], [b('a2'), 2], [b('a3'), 3], [b('a4'), 4]]

    def test_zunionstore_with_weight(self):
        self.arp('/ZADD/a/', {'scores': [('a1', 1), ('a2', 1), ('a3', 1)]})
        self.arp('/ZADD/b/', {'scores': [('a1', 2), ('a2', 2), ('a3', 2)]})
        self.arp('/ZADD/c/', {'scores': [('a1', 6), ('a3', 5), ('a4', 4)]})
        assert self.arp('/ZUNIONSTORE/', {'dest': 'd', 'keys': {'a': 1, 'b': 2, 'c': 3}}) == 4
        assert self.arg('/ZRANGE/d/0/-1/', params=[('withscores', 1)]) == \
            [[b('a2'), 5], [b('a4'), 12], [b('a3'), 20], [b('a1'), 23]]

    ### HASH COMMANDS ###
    def test_hget_and_hset(self):
        self.arp('/HMSET/a/', {'mapping': {'1': 1, '2': 2, '3': 3}})
        assert self.arg('/HGET/a/1/') == b('1')
        assert self.arg('/HGET/a/2/') == b('2')
        assert self.arg('/HGET/a/3/') == b('3')

        # field was updated redis returns 0
        assert self.arp('/HSET/a/2/', {'value': '5'}) == 0
        assert self.arg('/HGET/a/2/') == b('5')

        # field is new redis returns 1
        assert self.arp('/HSET/a/4/', {'value': '4'}) == 1
        assert self.arg('/HGET/a/4/') == b('4')

        # key inside of hash that doesn't exist returns null value
        assert self.arg('/HGET/a/b/') is None

    def test_hdel(self):
        self.arp('/HMSET/a/', {'mapping': {'1': 1, '2': 2, '3': 3}})
        assert self.ard('/HDEL/a/', params=[('key', 2)]) == 1
        assert self.arg('/HGET/a/2/') is None
        assert self.ard('/HDEL/a/', params=[('key', 1), ('key', 3)]) == 2
        assert self.arg('/HLEN/a/') == 0

    def test_hexists(self):
        self.arp('/HMSET/a/', {'mapping': {'1': 1, '2': 2, '3': 3}})
        assert self.arg('/HEXISTS/a/1/')
        assert not self.arg('/HEXISTS/a/4/')

    def test_hgetall(self):
        h = {b('a1'): b('1'), b('a2'): b('2'), b('a3'): b('3')}
        self.arp('/HMSET/a/', {'mapping': h})
        assert self.arg('/HGETALL/a/') == h

    def test_hincrby(self):
        assert self.arp('/HINCRBY/a/1/') == 1
        assert self.arp('/HINCRBY/a/1/', {'amount': 2}) == 3
        assert self.arp('/HINCRBY/a/1/', {'amount': -2}) == 1

    def test_hincrbyfloat(self):
        assert self.arp('/HINCRBYFLOAT/a/1/') == 1.0
        assert self.arp('/HINCRBYFLOAT/a/1/',) == 2.0
        assert self.arp('/HINCRBYFLOAT/a/1/', {'amount': 1.2}) == 3.2

    def test_hkeys(self):
        h = {b('a1'): b('1'), b('a2'): b('2'), b('a3'): b('3')}
        self.arp('/HMSET/a/', {'mapping': h})
        local_keys = h.keys()
        remote_keys = self.arg('/HKEYS/a/')
        assert (sorted(local_keys) == sorted(remote_keys))

    def test_hlen(self):
        self.arp('/HMSET/a/', {'mapping': {'1': 1, '2': 2, '3': 3}})
        assert self.arg('/HLEN/a/') == 3

    def test_hmget(self):
        self.arp('/HMSET/a/', {'mapping': {'a': 1, 'b': 2, 'c': 3}})
        assert self.arg('/HMGET/a/', params=[('key', 'a'), ('key', 'b'), ('key', 'c')]) == [b('1'), b('2'), b('3')]

    def test_hmset(self):
        h = {b('a'): b('1'), b('b'): b('2'), b('c'): b('3')}
        self.arp('/HMSET/a/', {'mapping': h})
        assert self.arg('/HGETALL/a/') == h

    def test_hsetnx(self):
        # Initially set the hash field
        assert self.arp('/HSETNX/a/', {'key': '1', 'value': '1'})
        assert self.arg('/HGET/a/1/') == '1'
        assert not self.arp('/HSETNX/a/', {'key': '1', 'value': '2'})
        assert self.arg('/HGET/a/1/') == '1'

    def test_hvals(self):
        h = {b('a1'): b('1'), b('a2'): b('2'), b('a3'): b('3')}
        self.arp('/HMSET/a/', {'mapping': h})
        local_vals = h.values()
        remote_vals = self.arg('/HVALS/a/')
        assert sorted(local_vals) == sorted(remote_vals)

    ### SORT ###
    def test_sort_basic(self):
        self.arp('/RPUSH/a/', {'values': ['3', '2', '1', '4']})
        assert self.arg('/SORT/a/') == [b('1'), b('2'), b('3'), b('4')]

    def test_sort_limited(self):
        self.arp('/RPUSH/a/', {'values': ['3', '2', '1', '4']})
        assert self.arg('/SORT/a/', params=[('start', 1), ('num', 2)]) == [b('2'), b('3')]

    def test_sort_by(self):
        self.arp('/SET/score:1/', {'value': '8'})
        self.arp('/SET/score:2/', {'value': '3'})
        self.arp('/SET/score:3/', {'value': '5'})
        self.arp('/RPUSH/a/', {'values': ['3', '2', '1']})
        assert self.arg('/SORT/a/', params=[('by', 'score:*')]) == [b('2'), b('3'), b('1')]

    def test_sort_get(self):
        self.arp('/SET/user:1/', {'value': 'u1'})
        self.arp('/SET/user:2/', {'value': 'u2'})
        self.arp('/SET/user:3/', {'value': 'u3'})
        self.arp('/RPUSH/a/', {'values': ['2', '3', '1']})
        assert self.arg('/SORT/a/', params=[('get', 'user:*')]) == [b('u1'), b('u2'), b('u3')]

    def test_sort_get_multi(self):
        self.arp('/SET/user:1/', {'value': 'u1'})
        self.arp('/SET/user:2/', {'value': 'u2'})
        self.arp('/SET/user:3/', {'value': 'u3'})
        self.arp('/RPUSH/a/', {'values': ['2', '3', '1']})
        assert self.arg('/SORT/a/', params=[('get', 'user:*'), ('get', '#')]) == \
            [b('u1'), b('1'), b('u2'), b('2'), b('u3'), b('3')]

    def test_sort_get_groups_two(self):
        self.arp('/SET/user:1/', {'value': 'u1'})
        self.arp('/SET/user:2/', {'value': 'u2'})
        self.arp('/SET/user:3/', {'value': 'u3'})
        self.arp('/RPUSH/a/', {'values': ['2', '3', '1']})
        assert self.arg('/SORT/a/', params=[('get', 'user:*'), ('get', '#'), ('groups', 1)]) == \
            [[b('u1'), b('1')], [b('u2'), b('2')], [b('u3'), b('3')]]

    def test_sort_groups_string_get(self):
        self.arp('/SET/user:1/', {'value': 'u1'})
        self.arp('/SET/user:2/', {'value': 'u2'})
        self.arp('/SET/user:3/', {'value': 'u3'})
        self.arp('/RPUSH/a/', {'values': ['2', '3', '1']})
        self.arg('/SORT/a/', params=[('get', 'user:*'), ('groups', 1)], assert_status_code=400,
                 error_string='when using "groups" the "get" argument must be specified and contain at least two keys')

    def test_sort_desc(self):
        self.arp('/RPUSH/a/', {'values': ['2', '3', '1']})
        assert self.arg('/SORT/a/', params=[('desc', 1)]) == [b('3'), b('2'), b('1')]

    def test_sort_alpha(self):
        self.arp('/RPUSH/a/', {'values': ['e', 'c', 'b', 'd', 'a']})
        assert self.arg('/SORT/a/', params=[('alpha', 1)]) == \
            [b('a'), b('b'), b('c'), b('d'), b('e')]

    def test_sort_store(self):
        self.arp('/RPUSH/a/', {'values': ['2', '3', '1']})
        assert self.arg('/SORT/a/', params=[('store', 'sorted_values')]) == 3
        assert self.arg('/LRANGE/sorted_values/0/-1/') == [b('1'), b('2'), b('3')]

# class TestStrictCommands(object):

#     def test_strict_zadd(self, sr):
#         sr.zadd('a', 1.0, 'a1', 2.0, 'a2', a3=3.0)
#         assert sr.zrange('a', 0, -1, withscores=True) == \
#             [(b('a1'), 1.0), (b('a2'), 2.0), (b('a3'), 3.0)]

#     def test_strict_lrem(self, sr):
#         sr.rpush('a', 'a1', 'a2', 'a3', 'a1')
#         sr.lrem('a', 0, 'a1')
#         assert sr.lrange('a', 0, -1) == [b('a2'), b('a3')]

#     def test_strict_setex(self, sr):
#         assert sr.setex('a', 60, '1')
#         assert sr['a'] == b('1')
#         assert 0 < sr.ttl('a') <= 60

#     def test_strict_ttl(self, sr):
#         assert not sr.expire('a', 10)
#         sr['a'] = '1'
#         assert sr.expire('a', 10)
#         assert 0 < sr.ttl('a') <= 10
#         assert sr.persist('a')
#         assert sr.ttl('a') == -1

#     @skip_if_server_version_lt('2.6.0')
#     def test_strict_pttl(self, sr):
#         assert not sr.pexpire('a', 10000)
#         sr['a'] = '1'
#         assert sr.pexpire('a', 10000)
#         assert 0 < sr.pttl('a') <= 10000
#         assert sr.persist('a')
#         assert sr.pttl('a') == -1


# class TestBinarySave(object):
#     def test_binary_get_set(self):
#         assert r.set(' foo bar ', '123')
#         assert r.get(' foo bar ') == b('123')

#         assert r.set(' foo\r\nbar\r\n ', '456')
#         assert r.get(' foo\r\nbar\r\n ') == b('456')

#         assert r.set(' \r\n\t\x07\x13 ', '789')
#         assert r.get(' \r\n\t\x07\x13 ') == b('789')

#         assert sorted(r.keys('*')) == \
#             [b(' \r\n\t\x07\x13 '), b(' foo\r\nbar\r\n '), b(' foo bar ')]

#         assert r.delete(' foo bar ')
#         assert r.delete(' foo\r\nbar\r\n ')
#         assert r.delete(' \r\n\t\x07\x13 ')

#     def test_binary_lists(self):
#         mapping = {
#             b('foo bar'): [b('1'), b('2'), b('3')],
#             b('foo\r\nbar\r\n'): [b('4'), b('5'), b('6')],
#             b('foo\tbar\x07'): [b('7'), b('8'), b('9')],
#         }
#         # fill in lists
#         for key, value in iteritems(mapping):
#             r.rpush(key, *value)

#         # check that KEYS returns all the keys as they are
#         assert sorted(r.keys('*')) == sorted(list(iterkeys(mapping)))

#         # check that it is possible to get list content by key name
#         for key, value in iteritems(mapping):
#             assert r.lrange(key, 0, -1) == value

#     def test_22_info(self):
#         """
#         Older Redis versions contained 'allocation_stats' in INFO that
#         was the cause of a number of bugs when parsing.
#         """
#         info = "allocation_stats:6=1,7=1,8=7141,9=180,10=92,11=116,12=5330," \
#                "13=123,14=3091,15=11048,16=225842,17=1784,18=814,19=12020," \
#                "20=2530,21=645,22=15113,23=8695,24=142860,25=318,26=3303," \
#                "27=20561,28=54042,29=37390,30=1884,31=18071,32=31367,33=160," \
#                "34=169,35=201,36=10155,37=1045,38=15078,39=22985,40=12523," \
#                "41=15588,42=265,43=1287,44=142,45=382,46=945,47=426,48=171," \
#                "49=56,50=516,51=43,52=41,53=46,54=54,55=75,56=647,57=332," \
#                "58=32,59=39,60=48,61=35,62=62,63=32,64=221,65=26,66=30," \
#                "67=36,68=41,69=44,70=26,71=144,72=169,73=24,74=37,75=25," \
#                "76=42,77=21,78=126,79=374,80=27,81=40,82=43,83=47,84=46," \
#                "85=114,86=34,87=37,88=7240,89=34,90=38,91=18,92=99,93=20," \
#                "94=18,95=17,96=15,97=22,98=18,99=69,100=17,101=22,102=15," \
#                "103=29,104=39,105=30,106=70,107=22,108=21,109=26,110=52," \
#                "111=45,112=33,113=67,114=41,115=44,116=48,117=53,118=54," \
#                "119=51,120=75,121=44,122=57,123=44,124=66,125=56,126=52," \
#                "127=81,128=108,129=70,130=50,131=51,132=53,133=45,134=62," \
#                "135=12,136=13,137=7,138=15,139=21,140=11,141=20,142=6,143=7," \
#                "144=11,145=6,146=16,147=19,148=1112,149=1,151=83,154=1," \
#                "155=1,156=1,157=1,160=1,161=1,162=2,166=1,169=1,170=1,171=2," \
#                "172=1,174=1,176=2,177=9,178=34,179=73,180=30,181=1,185=3," \
#                "187=1,188=1,189=1,192=1,196=1,198=1,200=1,201=1,204=1,205=1," \
#                "207=1,208=1,209=1,214=2,215=31,216=78,217=28,218=5,219=2," \
#                "220=1,222=1,225=1,227=1,234=1,242=1,250=1,252=1,253=1," \
#                ">=256=203"
#         parsed = parse_info(info)
#         assert 'allocation_stats' in parsed
#         assert '6' in parsed['allocation_stats']
#         assert '>=256' in parsed['allocation_stats']

#     def test_large_responses(self):
#         "The PythonParser has some special cases for return values > 1MB"
#         # load up 5MB of data into a key
#         data = ''.join([ascii_letters] * (5000000 // len(ascii_letters)))
#         r['a'] = data
#         assert r['a'] == b(data)

#     def test_floating_point_encoding(self):
#         """
#         High precision floating point values sent to the server should keep
#         precision.
#         """
#         timestamp = 1349673917.939762
#         r.zadd('a', 'a1', timestamp)
#         assert r.zscore('a', 'a1') == timestamp