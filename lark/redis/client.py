from collections import namedtuple
import schemas


DEFAULT_INBOUND_SCHEMA = schemas.NoSchema
DEFAULT_OUTBOUND_SCHEMA = schemas.OutboundResultSchema


class RedisApiClientException(Exception):
    pass


class RedisApiClientAuthException(RedisApiClientException):
    pass


class RedisApiClient(object):

    @classmethod
    def from_request(cls, redis_method, r, request_json, get_query_dict, url_args, url_kwargs, request_scopes=set([])):
        redis_api_client = cls()

        # Check that method exisits
        try:
            redis_method_def = getattr(redis_api_client, redis_method)
        except AttributeError:
            raise RedisApiClientException('%s is not a redis method' % redis_method)

        # Check scopes
        has_scopes = request_scopes & redis_method_def.scopes
        if len(has_scopes) == 0:
            raise RedisApiClientAuthException('Request has %s scopes and is required to have at least one of %s scopes' % (request_scopes, redis_method_def.scopes))

        # Parse request for redis args
        redis_args, redis_kwargs = redis_api_client.get_signature_from_request(redis_method_def, request_json, get_query_dict, url_args, url_kwargs)

        # Execute redis method
        data = getattr(r, redis_method)(*redis_args, **redis_kwargs)

        # Transform redis data into outbounc data format
        response_data = redis_api_client.format_redis_response_for_http(redis_method_def, data)

        return response_data

    def get_signature_from_request(self, redis_method_def, request_json, get_query_dict, url_args, url_kwargs):
        # print 'args %s', % list(url_args)
        # print 'kwargs %s', % url_kwargs
        # print 'request.args %s', % get_query_dict
        # print 'request_json %s', % request_json

        InboundSchema = redis_method_def.inbound

        args, kwargs = InboundSchema.from_request(url_args, url_kwargs, get_query_dict, request_json)
        return (args, kwargs)

    def format_redis_response_for_http(self, redis_method_def, data):
        data = redis_method_def.outbound.serialize(data)

        return data


_RedisMethodDef = namedtuple('RedisMethodDef', 'method inbound outbound cmd_type write read')


class RedisMethodDef(_RedisMethodDef):

    @classmethod
    def from_kwargs(cls, method, inbound, outbound, cmd_type, write, read):
        if write == read:
            raise Exception("Command %s has to be write or read" % (cmd_type))

        return cls(inbound, outbound)

    @property
    def scopes(self):
        scopes = set(['admin'])
        if self.cmd_type != 'admin':
            scopes.add('%s:*' % self.cmd_type)

        if self.read:
            scopes.add('read:*')
            scopes.add('read:%s' % (self.method))

        if self.write:
            scopes.add('write:*')
            scopes.add('write:%s' % (self.method))

        return scopes


def bind_api_method(method, inbound=DEFAULT_INBOUND_SCHEMA, outbound=DEFAULT_OUTBOUND_SCHEMA, cmd_type='admin', write=False, read=False):
    redis_method_def = RedisMethodDef(method, inbound, outbound, cmd_type, write, read)

    def run(self, *args, **kwargs):
        return redis_method_def

    ctx = {
        'cmd': method,
        'scopes': ', '.join(map(lambda x: '**%s**' % x, list(redis_method_def.scopes))),
    }
    doc = """
    redis docs for `%(cmd)s <http://redis.io/commands/%(cmd)s>`_

    Requires one of these scopes: %(scopes)s

    """ % ctx

    run.__doc__ = doc
    run = property(run)
    setattr(RedisApiClient, method, run)


# Admin commands
bind_api_method('bgrewriteaof', write=True)
bind_api_method('client_list', read=True)
bind_api_method('bgsave', write=True)
bind_api_method('client_getname', read=True)
bind_api_method('client_setname', write=True, inbound=schemas.NameSchema)
bind_api_method('client_kill', write=True, inbound=schemas.AddressSchema)
bind_api_method('config_get', inbound=schemas.PatternSchema)
bind_api_method('config_set', inbound=schemas.NameValueSchema)
bind_api_method('config_resetstat', write=True)
bind_api_method('dbsize', read=True)
bind_api_method('flushall', write=True)
bind_api_method('flushdb', write=True)
bind_api_method('lastsave', read=True)
bind_api_method('save', write=True)
bind_api_method('debug_object', read=True, inbound=schemas.KeySchema)
bind_api_method('object', read=True, inbound=schemas.InfotypeKeyScheam)
bind_api_method('info', read=True, inbound=schemas.SectionSchema)
bind_api_method('ping', cmd_type='basic', read=True)
bind_api_method('echo', cmd_type='basic', read=True, inbound=schemas.ValueSchema)
bind_api_method('dump', read=True, inbound=schemas.NameSchema, outbound=schemas.OutBoundBinaryValueSchema)
bind_api_method('restore', write=True, inbound=schemas.NameTtlBinValueSchema)

# Keys
bind_api_method('randomkey', cmd_type='key', read=True)
bind_api_method('get', cmd_type='key', read=True, inbound=schemas.KeySchema, outbound=schemas.OutboundValueSchema)
bind_api_method('set', cmd_type='key', write=True, inbound=schemas.SetSchema)
bind_api_method('append', cmd_type='key', write=True, inbound=schemas.KeyValueSchema)
bind_api_method('setbit', cmd_type='key', write=True, inbound=schemas.NameOffsetBoolValueSchema)
bind_api_method('bitcount', cmd_type='key', read=True, inbound=schemas.KeyRangeOptionalSchema)
bind_api_method('bitop', cmd_type='key', write=True, inbound=schemas.OperationDestKeysSchema)
bind_api_method('decr', cmd_type='key', write=True, inbound=schemas.NameAmountSchema)
bind_api_method('delete', cmd_type='key', write=True, inbound=schemas.NamesSchema)
bind_api_method('exists', cmd_type='key', read=True, inbound=schemas.KeySchema)
bind_api_method('expire', cmd_type='key', write=True, inbound=schemas.NameTimeSchema)
bind_api_method('expireat', cmd_type='key', write=True, inbound=schemas.NameWhenSchema)
bind_api_method('ttl', cmd_type='key', read=True, inbound=schemas.NameSchema)
bind_api_method('pexpire', cmd_type='key', write=True, inbound=schemas.NameTimeSchema)
bind_api_method('pexpireat', cmd_type='key', write=True, inbound=schemas.NameWhenSchema)
bind_api_method('pttl', cmd_type='key', read=True, inbound=schemas.NameSchema)
bind_api_method('psetex', cmd_type='key', write=True, inbound=schemas.NameTimeMsValueSchema)
bind_api_method('persist', cmd_type='key', write=True, inbound=schemas.NameSchema)
bind_api_method('getbit', cmd_type='key', read=True, inbound=schemas.NameOffsetSchema)
bind_api_method('getrange', cmd_type='key', read=True, inbound=schemas.KeyRangeSchema)
bind_api_method('getset', cmd_type='key', read=True, inbound=schemas.NameValueSchema)
bind_api_method('incr', cmd_type='key', write=True, inbound=schemas.NameAmountSchema, outbound=schemas.OutboundResultSchema)
bind_api_method('incrbyfloat', cmd_type='key', inbound=schemas.NameFloatAmountSchema, outbound=schemas.OutboundResultSchema)
bind_api_method('keys', cmd_type='key', read=True, inbound=schemas.PatternSchema)
bind_api_method('mget', cmd_type='key', read=True, inbound=schemas.KeyListSchema)
bind_api_method('mset', cmd_type='key', write=True, inbound=schemas.NameValueListSchema, outbound=schemas.OutboundValueSchema)
bind_api_method('msetnx', cmd_type='key', write=True, inbound=schemas.NameValueListSchema, outbound=schemas.OutboundValueSchema)
bind_api_method('rename', cmd_type='key', write=True, inbound=schemas.SrcDstSchema)
bind_api_method('renamenx', cmd_type='key', write=True, inbound=schemas.SrcDstSchema)
bind_api_method('setex', cmd_type='key', write=True, inbound=schemas.NameValueTimeSchema, outbound=schemas.OutboundValueSchema)
bind_api_method('setnx', cmd_type='key', write=True, inbound=schemas.NameValueSchema, outbound=schemas.OutboundValueSchema)
bind_api_method('setrange', cmd_type='key', inbound=schemas.NameOffsetStrValueSchema)
bind_api_method('strlen', cmd_type='key', read=True, inbound=schemas.NameSchema)
bind_api_method('substr', cmd_type='key', read=True, inbound=schemas.NameRangeEndOptionalSchema, outbound=schemas.OutboundValueSchema)
bind_api_method('type', cmd_type='key', read=True, inbound=schemas.NameSchema)

# Lists
bind_api_method('blpop', cmd_type='list', write=True, inbound=schemas.KeysTimeoutSchema)
bind_api_method('brpop', cmd_type='list', write=True, inbound=schemas.KeysTimeoutSchema)
bind_api_method('brpoplpush', cmd_type='list', write=True, inbound=schemas.SrcDstTimeoutSchema)
bind_api_method('lindex', cmd_type='list', read=True, inbound=schemas.NameIndexSchema)
bind_api_method('linsert', cmd_type='list', write=True, inbound=schemas.NameWhereRefValueValueSchema)
bind_api_method('llen', cmd_type='list', read=True, inbound=schemas.NameSchema)
bind_api_method('lpop', cmd_type='list', write=True, inbound=schemas.NameSchema)
bind_api_method('lpush', cmd_type='list', write=True, inbound=schemas.NameValuesSchema)
bind_api_method('lpushx', cmd_type='list', write=True, inbound=schemas.NameValueSchema)
bind_api_method('lrange', cmd_type='list', read=True, inbound=schemas.NameRangeSchema)
bind_api_method('lrem', cmd_type='list', write=True, inbound=schemas.NameNumValueSchema)
bind_api_method('lset', cmd_type='list', write=True, inbound=schemas.NameIndexValueSchema)
bind_api_method('ltrim', cmd_type='list', write=True, inbound=schemas.NameRangeSchema)
bind_api_method('rpop', cmd_type='list', write=True, inbound=schemas.NameSchema)
bind_api_method('rpoplpush', cmd_type='list', write=True, inbound=schemas.SrcDstSchema)
bind_api_method('rpush', cmd_type='list', write=True, inbound=schemas.NameValuesSchema)
bind_api_method('rpushx', cmd_type='list', write=True, inbound=schemas.NameValueSchema)

# Sorting
bind_api_method('sort', cmd_type='sort', write=True, inbound=schemas.SortSchema)

# Scaning
bind_api_method('scan', cmd_type='scan', read=True, inbound=schemas.ScanSchema)
bind_api_method('sscan', cmd_type='scan', read=True, inbound=schemas.NameScanSchema)
bind_api_method('hscan', cmd_type='scan', read=True, inbound=schemas.NameScanSchema)
bind_api_method('zscan', cmd_type='scan', read=True, inbound=schemas.NameScanSchema)

# Sets
bind_api_method('sadd', cmd_type='sets', write=True, inbound=schemas.NameValuesSchema)
bind_api_method('smembers', cmd_type='sets', read=True, inbound=schemas.NameSchema)
bind_api_method('scard', cmd_type='sets', read=True, inbound=schemas.NameSchema)
bind_api_method('sdiff', cmd_type='sets', read=True, inbound=schemas.KeysSchema)
bind_api_method('sdiffstore', cmd_type='sets', write=True, inbound=schemas.DestKeysSchema)
bind_api_method('sinter', cmd_type='sets', read=True, inbound=schemas.KeysSchema)
bind_api_method('sinterstore', cmd_type='sets', write=True, inbound=schemas.DestKeysSchema)
bind_api_method('sismember', cmd_type='sets', read=True, inbound=schemas.NameValueSchema)
bind_api_method('smove', cmd_type='sets', write=True, inbound=schemas.SrcDstValueSchema)
bind_api_method('spop', cmd_type='sets', write=True, inbound=schemas.NameSchema)
bind_api_method('srandmember', cmd_type='sets', read=True, inbound=schemas.NameNumberSchema)
bind_api_method('srem', cmd_type='sets', write=True, inbound=schemas.RemNameValueListSchema)
bind_api_method('sunion', cmd_type='sets', read=True, inbound=schemas.KeysSchema)
bind_api_method('sunionstore', cmd_type='sets', write=True, inbound=schemas.DestKeysSchema)

# Sorted Sets
bind_api_method('zadd', cmd_type='sorted_sets', write=True, inbound=schemas.NameScoreListSchema)
bind_api_method('zcard', cmd_type='sorted_sets', read=True, inbound=schemas.NameSchema)
bind_api_method('zcount', cmd_type='sorted_sets', read=True, inbound=schemas.NameMinMaxSchema)
bind_api_method('zincrby', cmd_type='sorted_sets', write=True, inbound=schemas.NameValueAmount)
bind_api_method('zinterstore', cmd_type='sorted_sets', write=True, inbound=schemas.DestKeysAggregateSchema)
bind_api_method('zrange', cmd_type='sorted_sets', read=True, inbound=schemas.ZrangeSchema)
bind_api_method('zrangebyscore', cmd_type='sorted_sets', read=True, inbound=schemas.ZrangeByScoresSchema)
bind_api_method('zrevrangebyscore', cmd_type='sorted_sets', read=True, inbound=schemas.ZrangeByScoresSchema)
bind_api_method('zrank', cmd_type='sorted_sets', read=True, inbound=schemas.NameValueSchema)
bind_api_method('zrevrank', cmd_type='sorted_sets', read=True, inbound=schemas.NameValueSchema)
bind_api_method('zrem', cmd_type='sorted_sets', write=True, inbound=schemas.RemNameValueListSchema)
bind_api_method('zremrangebyrank', cmd_type='sorted_sets', inbound=schemas.NameMinMaxSchema)
bind_api_method('zremrangebyscore', cmd_type='sorted_sets', inbound=schemas.NameMinMaxSchema)
bind_api_method('zrevrange', cmd_type='sorted_sets', read=True, inbound=schemas.ZrevRangeSchema)
bind_api_method('zscore', cmd_type='sorted_sets', read=True, inbound=schemas.NameValueSchema)
bind_api_method('zunionstore', cmd_type='sorted_sets', inbound=schemas.DestKeysAggregateSchema)

# Hashes
bind_api_method('hget', cmd_type='hashes', read=True, inbound=schemas.NameKeySchema)
bind_api_method('hgetall', cmd_type='hashes', read=True, inbound=schemas.NameSchema)
bind_api_method('hexists', cmd_type='hashes', read=True, inbound=schemas.NameKeySchema)
bind_api_method('hdel', cmd_type='hashes', write=True, inbound=schemas.NameKeysSchema)
bind_api_method('hincrby', cmd_type='hashes', write=True, inbound=schemas.NameKeyAmountSchema)
bind_api_method('hincrbyfloat', cmd_type='hashes', write=True, inbound=schemas.NameKeyFloatAmountSchema)
bind_api_method('hkeys', cmd_type='hashes', read=True, inbound=schemas.NameSchema)
bind_api_method('hlen', cmd_type='hashes', read=True, inbound=schemas.NameSchema)
bind_api_method('hset', cmd_type='hashes', write=True, inbound=schemas.NameKeyValueSchema)
bind_api_method('hsetnx', cmd_type='hashes', write=True, inbound=schemas.NameKeyValueSchema)
bind_api_method('hmset', cmd_type='hashes', write=True, inbound=schemas.NameMapingSchema)
bind_api_method('hmget', cmd_type='hashes', read=True, inbound=schemas.NameKeyListSchema)
bind_api_method('hvals', cmd_type='hashes', read=True, inbound=schemas.NameSchema)
