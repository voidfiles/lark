.. _redit_api_client

*********************
Core Redis API Client
*********************

The core redis API client is the main tool that maps from an http request to a redis call.

.. module:: adnpy.api

:mod:`lark.redis.client` --- App.net API
========================================
.. autoclass:: RedisApiClient


Admin Methods
=============

.. automethod:: lark.redis.client.RedisApiClient.bgrewriteaof
.. automethod:: lark.redis.client.RedisApiClient.client_list
.. automethod:: lark.redis.client.RedisApiClient.bgsave
.. automethod:: lark.redis.client.RedisApiClient.client_getname
.. automethod:: lark.redis.client.RedisApiClient.client_setname
.. automethod:: lark.redis.client.RedisApiClient.client_kill
.. automethod:: lark.redis.client.RedisApiClient.config_get
.. automethod:: lark.redis.client.RedisApiClient.config_set
.. automethod:: lark.redis.client.RedisApiClient.config_resetstat
.. automethod:: lark.redis.client.RedisApiClient.dbsize
.. automethod:: lark.redis.client.RedisApiClient.flushall
.. automethod:: lark.redis.client.RedisApiClient.flushdb
.. automethod:: lark.redis.client.RedisApiClient.lastsave
.. automethod:: lark.redis.client.RedisApiClient.save
.. automethod:: lark.redis.client.RedisApiClient.debug_object
.. automethod:: lark.redis.client.RedisApiClient.info
.. automethod:: lark.redis.client.RedisApiClient.ping
.. automethod:: lark.redis.client.RedisApiClient.echo


Key  Methods
============

.. automethod:: lark.redis.client.RedisApiClient.randomkey
.. automethod:: lark.redis.client.RedisApiClient.get
.. automethod:: lark.redis.client.RedisApiClient.set
.. automethod:: lark.redis.client.RedisApiClient.append
.. automethod:: lark.redis.client.RedisApiClient.setbit
.. automethod:: lark.redis.client.RedisApiClient.bitcount
.. automethod:: lark.redis.client.RedisApiClient.bitop
.. automethod:: lark.redis.client.RedisApiClient.decr
.. automethod:: lark.redis.client.RedisApiClient.delete
.. automethod:: lark.redis.client.RedisApiClient.dump
.. automethod:: lark.redis.client.RedisApiClient.restore
.. automethod:: lark.redis.client.RedisApiClient.exists
.. automethod:: lark.redis.client.RedisApiClient.expire
.. automethod:: lark.redis.client.RedisApiClient.expireat
.. automethod:: lark.redis.client.RedisApiClient.ttl
.. automethod:: lark.redis.client.RedisApiClient.pexpire
.. automethod:: lark.redis.client.RedisApiClient.pexpireat
.. automethod:: lark.redis.client.RedisApiClient.pttl
.. automethod:: lark.redis.client.RedisApiClient.psetex
.. automethod:: lark.redis.client.RedisApiClient.persist
.. automethod:: lark.redis.client.RedisApiClient.getbit
.. automethod:: lark.redis.client.RedisApiClient.getrange
.. automethod:: lark.redis.client.RedisApiClient.getset
.. automethod:: lark.redis.client.RedisApiClient.incr
.. automethod:: lark.redis.client.RedisApiClient.incrbyfloat
.. automethod:: lark.redis.client.RedisApiClient.keys
.. automethod:: lark.redis.client.RedisApiClient.mget
.. automethod:: lark.redis.client.RedisApiClient.mset
.. automethod:: lark.redis.client.RedisApiClient.msetnx
.. automethod:: lark.redis.client.RedisApiClient.rename
.. automethod:: lark.redis.client.RedisApiClient.renamenx
.. automethod:: lark.redis.client.RedisApiClient.setex
.. automethod:: lark.redis.client.RedisApiClient.setnx
.. automethod:: lark.redis.client.RedisApiClient.setrange
.. automethod:: lark.redis.client.RedisApiClient.strlen
.. automethod:: lark.redis.client.RedisApiClient.substr
.. automethod:: lark.redis.client.RedisApiClient.type


List Methods
============

.. automethod:: lark.redis.client.RedisApiClient.blpop
.. automethod:: lark.redis.client.RedisApiClient.brpop
.. automethod:: lark.redis.client.RedisApiClient.brpoplpush
.. automethod:: lark.redis.client.RedisApiClient.lindex
.. automethod:: lark.redis.client.RedisApiClient.linsert
.. automethod:: lark.redis.client.RedisApiClient.llen
.. automethod:: lark.redis.client.RedisApiClient.lpop
.. automethod:: lark.redis.client.RedisApiClient.lpush
.. automethod:: lark.redis.client.RedisApiClient.lpushx
.. automethod:: lark.redis.client.RedisApiClient.lrange
.. automethod:: lark.redis.client.RedisApiClient.lrem
.. automethod:: lark.redis.client.RedisApiClient.lset
.. automethod:: lark.redis.client.RedisApiClient.ltrim
.. automethod:: lark.redis.client.RedisApiClient.rpop
.. automethod:: lark.redis.client.RedisApiClient.rpoplpush
.. automethod:: lark.redis.client.RedisApiClient.rpush
.. automethod:: lark.redis.client.RedisApiClient.rpushx


Sort Method
===========

.. automethod:: lark.redis.client.RedisApiClient.sort


Scan Method
===========

.. automethod:: lark.redis.client.RedisApiClient.scan
.. automethod:: lark.redis.client.RedisApiClient.sscan
.. automethod:: lark.redis.client.RedisApiClient.hscan
.. automethod:: lark.redis.client.RedisApiClient.zscan


Set Methods
===========

.. automethod:: lark.redis.client.RedisApiClient.sadd
.. automethod:: lark.redis.client.RedisApiClient.smembers
.. automethod:: lark.redis.client.RedisApiClient.scard
.. automethod:: lark.redis.client.RedisApiClient.sdiff
.. automethod:: lark.redis.client.RedisApiClient.sdiffstore
.. automethod:: lark.redis.client.RedisApiClient.sinter
.. automethod:: lark.redis.client.RedisApiClient.sinterstore
.. automethod:: lark.redis.client.RedisApiClient.sismember
.. automethod:: lark.redis.client.RedisApiClient.smove
.. automethod:: lark.redis.client.RedisApiClient.spop
.. automethod:: lark.redis.client.RedisApiClient.srandmember
.. automethod:: lark.redis.client.RedisApiClient.srem
.. automethod:: lark.redis.client.RedisApiClient.sunion
.. automethod:: lark.redis.client.RedisApiClient.sunionstore


Sorted Set Methods
==================

.. automethod:: lark.redis.client.RedisApiClient.zadd
.. automethod:: lark.redis.client.RedisApiClient.zcard
.. automethod:: lark.redis.client.RedisApiClient.zcount
.. automethod:: lark.redis.client.RedisApiClient.zincrby
.. automethod:: lark.redis.client.RedisApiClient.zinterstore
.. automethod:: lark.redis.client.RedisApiClient.zrange
.. automethod:: lark.redis.client.RedisApiClient.zrangebyscore
.. automethod:: lark.redis.client.RedisApiClient.zrevrangebyscore
.. automethod:: lark.redis.client.RedisApiClient.zrank
.. automethod:: lark.redis.client.RedisApiClient.zrevrank
.. automethod:: lark.redis.client.RedisApiClient.zrem
.. automethod:: lark.redis.client.RedisApiClient.zremrangebyrank
.. automethod:: lark.redis.client.RedisApiClient.zremrangebyscore
.. automethod:: lark.redis.client.RedisApiClient.zrevrange
.. automethod:: lark.redis.client.RedisApiClient.zscore
.. automethod:: lark.redis.client.RedisApiClient.zunionstore


Hash Methods
============

.. automethod:: lark.redis.client.RedisApiClient.hget
.. automethod:: lark.redis.client.RedisApiClient.hgetall
.. automethod:: lark.redis.client.RedisApiClient.hexists
.. automethod:: lark.redis.client.RedisApiClient.hdel
.. automethod:: lark.redis.client.RedisApiClient.hincrby
.. automethod:: lark.redis.client.RedisApiClient.hincrbyfloat
.. automethod:: lark.redis.client.RedisApiClient.hkeys
.. automethod:: lark.redis.client.RedisApiClient.hlen
.. automethod:: lark.redis.client.RedisApiClient.hset
.. automethod:: lark.redis.client.RedisApiClient.hsetnx
.. automethod:: lark.redis.client.RedisApiClient.hmset
.. automethod:: lark.redis.client.RedisApiClient.hmget
.. automethod:: lark.redis.client.RedisApiClient.hvals

