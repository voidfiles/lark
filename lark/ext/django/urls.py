from django.conf.urls import patterns, url
import re

urlpatterns = []


def build_api_func(routes, methods=['GET'], redispy_method=None):
    if isinstance(routes, basestring):
        routes = [routes]

    if not redispy_method:
        redispy_method = routes[0][1:].split('/')[0].lower()

    for route in routes:
        args = re.findall(r'(<\w+>)', route)
        for arg in args:
            name = '(?P<%s>[^/]+)' % (arg[1:-1])
            route = route.replace(arg, name, 1)
        # print route
        urlpatterns.append(url(r'(?i)^%s$' % (route[1:]), 'lark.ext.django.views.query_redis', {'redispy_method': redispy_method, 'methods': methods}))


build_api_func('/BGREWRITEAOF/')

build_api_func('/BGSAVE/')

build_api_func('/CLIENT/LIST/', redispy_method='client_list')

build_api_func('/CLIENT/KILL/', methods=['POST'], redispy_method='client_kill')

build_api_func('/CLIENT/GETNAME/', redispy_method='client_getname')

build_api_func('/CLIENT/SETNAME/', methods=['POST'], redispy_method='client_setname')

build_api_func(['/CONFIG/GET/<pattern>', '/CONFIG/GET/'], redispy_method='config_get')

build_api_func('/CONFIG/SET/<name>/', methods=['POST'], redispy_method='config_set')

build_api_func('/CONFIG/RESETSTAT/', methods=['POST'], redispy_method='config_resetstat')

build_api_func('/DBSIZE/')

build_api_func('/DEBUG/OBJECT/<key>', redispy_method='debug_object')

build_api_func('/ECHO/', methods=['POST'])

build_api_func('/FLUSHALL/', methods=['DELETE'])

build_api_func('/FLUSHDB/', methods=['DELETE'])

build_api_func(['/INFO/<section>', '/INFO/'])

build_api_func('/LASTSAVE/')

build_api_func('/OBJECT/<infotype>/<key>/')

build_api_func('/PING/')

build_api_func('/SAVE/')

build_api_func('/DUMP/<name>/')

build_api_func('/RESTORE/<name>/', methods=['POST'])

# Strings
build_api_func('/GET/<key>/')

build_api_func('/SET/<key>/', methods=['POST'])

build_api_func('/APPEND/<key>/', methods=['POST'])

build_api_func('/SETBIT/<name>/', methods=['POST'])

build_api_func(['/BITCOUNT/<key>/<start>/<end>/', '/BITCOUNT/<key>/'])

build_api_func('/BITOP/', methods=['POST'])

build_api_func(['/DECR/<name>/', '/DECRBY/<name>/'], methods=['POST'], redispy_method='decr')

build_api_func(['/DEL/<name>/', '/DEL/'], methods=['DELETE'], redispy_method='delete')

build_api_func('/EXISTS/<key>/')

build_api_func('/EXPIRE/<name>/', methods=['POST'])

build_api_func('/EXPIREAT/<name>/', methods=['POST'])

build_api_func('/TTL/<name>/')

build_api_func('/PEXPIRE/<name>/', methods=['POST'])

build_api_func('/PEXPIREAT/<name>/', methods=['POST'])

build_api_func('/PTTL/<name>/')

build_api_func('/PSETEX/<name>/', methods=['POST'])

build_api_func('/PERSIST/<name>/', methods=['POST'])

build_api_func('/GETBIT/<name>/<offset>/')

build_api_func('/GETRANGE/<key>/<start>/<end>/')

build_api_func('/GETSET/<name>/', methods=['POST'])

build_api_func(['/INCR/<name>/', '/INCRBY/<name>/'], methods=['POST'], redispy_method='incr')

build_api_func('/INCRBYFLOAT/<name>/', methods=['POST'])

build_api_func(['/KEYS/<pattern>/', '/KEYS/'], redispy_method='keys')

build_api_func('/MGET/')

build_api_func('/MSET/', methods=['POST'])

build_api_func('/MSETNX/', methods=['POST'])

build_api_func('/RANDOMKEY/')

build_api_func('/RENAME/', methods=['POST'])

build_api_func('/RENAMENX/', methods=['POST'])

build_api_func('/SETEX/<name>/', methods=['POST'])

build_api_func('/SETNX/<name>/', methods=['POST'])

build_api_func('/SETRANGE/<name>/', methods=['POST'])

build_api_func('/STRLEN/<name>/')

build_api_func(['/SUBSTR/<name>/<start>/<end>/', '/SUBSTR/<name>/<start>/'])

build_api_func('/TYPE/<name>/')

build_api_func('/BLPOP/', methods=['POST'])

build_api_func('/BRPOP/', methods=['POST'])

build_api_func('/BRPOPLPUSH/', methods=['POST'])

build_api_func('/LINDEX/<name>/<index>/')

build_api_func('/LINSERT/<name>/', methods=['POST'])

build_api_func('/LLEN/<name>/')

build_api_func('/LPOP/<name>/', methods=['POST'])

build_api_func('/LPUSH/<name>/', methods=['POST'])

build_api_func('/LPUSHX/<name>/', methods=['POST'])

build_api_func('/LRANGE/<name>/<start>/<end>/', )

build_api_func(['/LREM/<name>/<value>/<num>/', '/LREM/<name>/<value>/'], methods=['DELETE'])

build_api_func('/LSET/<name>/', methods=['POST'])

build_api_func('/LTRIM/<name>/<start>/<end>/', methods=['DELETE'])

build_api_func('/RPOP/<name>/', methods=['POST'])

build_api_func('/RPOPLPUSH/', methods=['POST'])

build_api_func('/RPUSH/<name>/', methods=['POST'])

build_api_func('/RPUSHX/<name>/', methods=['POST'])

build_api_func('/SORT/<name>/')

build_api_func('/SCAN/')

build_api_func('/SSCAN/<name>/')

build_api_func('/HSCAN/<name>/')

build_api_func('/ZSCAN/<name>/')

build_api_func('/SADD/<name>/', methods=['POST'])

build_api_func('/SMEMBERS/<name>/')

build_api_func('/SCARD/<name>/')

build_api_func('/SDIFF/')

build_api_func('/SDIFFSTORE/', methods=['POST'])

build_api_func('/SINTER/')

build_api_func('/SINTERSTORE/', methods=['POST'])

build_api_func('/SISMEMBER/<name>/<value>/')

build_api_func('/SMOVE/', methods=['POST'])

build_api_func('/SPOP/<name>/', methods=['POST'])

build_api_func(['/SRANDMEMBER/<name>/<number>/', '/SRANDMEMBER/<name>/'])

build_api_func('/SREM/<name>/', methods=['DELETE'])

build_api_func('/SUNION/')

build_api_func('/SUNIONSTORE/', methods=['POST'])

build_api_func('/ZADD/<name>/', methods=['POST'])

build_api_func('/ZCARD/<name>/')

build_api_func('/ZCOUNT/<name>/<min>/<max>/')

build_api_func('/ZINCRBY/<name>/', methods=['POST'])

build_api_func('/ZINTERSTORE/', methods=['POST'])

build_api_func('/ZRANGE/<name>/<start>/<end>/')

build_api_func('/ZRANGEBYSCORE/<name>/<min>/<max>/')

build_api_func('/ZREVRANGEBYSCORE/<name>/<min>/<max>/')

build_api_func('/ZRANK/<name>/<value>/')

build_api_func('/ZREVRANK/<name>/<value>/')

build_api_func('/ZREM/<name>/', methods=['DELETE'])

build_api_func('/ZREMRANGEBYRANK/<name>/<min>/<max>/', methods=['DELETE'])

build_api_func('/ZREMRANGEBYSCORE/<name>/<min>/<max>/', methods=['DELETE'])

build_api_func('/ZREVRANGE/<name>/<start>/<end>/')

build_api_func('/ZSCORE/<name>/<value>/')

build_api_func('/ZUNIONSTORE/', methods=['POST'])

build_api_func('/HGET/<name>/<key>/')

build_api_func('/HGETALL/<name>/')

build_api_func('/HEXISTS/<name>/<key>/')

build_api_func('/HDEL/<name>/', methods=['DELETE'])

build_api_func('/HINCRBY/<name>/<key>/', methods=['POST'])

build_api_func('/HINCRBYFLOAT/<name>/<key>/', methods=['POST'])

build_api_func('/HKEYS/<name>/')

build_api_func('/HLEN/<name>/')

build_api_func('/HSET/<name>/<key>/', methods=['POST'])

build_api_func('/HSETNX/<name>/', methods=['POST'])

build_api_func('/HMSET/<name>/', methods=['POST'])

build_api_func('/HMGET/<name>/')

build_api_func('/HVALS/<name>/')

urlpatterns = patterns('', *urlpatterns)
