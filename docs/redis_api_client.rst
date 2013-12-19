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

.. autoattribute:: lark.redis.client.RedisApiClient.bgrewriteaof

::

	POST /BGWRITEAOF/

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.client_list

::

	GET /CLIENT/LIST/

	output: {u'data': [{u'addr': u'127.0.0.1:54188',
	            u'age': u'1036279',
	            u'cmd': u'monitor',
	            u'db': u'0',
	            u'events': u'rw',
	            u'fd': u'6',
	            u'flags': u'O',
	            u'idle': u'0',
	            u'multi': u'-1',
	            u'name': u'',
	            u'obl': u'57',
	            u'oll': u'0',
	            u'omem': u'0',
	            u'psub': u'0',
	            u'qbuf': u'0',
	            u'qbuf-free': u'0',
	            u'sub': u'0'},
	           {u'addr': u'127.0.0.1:51684',
	            u'age': u'0',
	            u'cmd': u'client',
	            u'db': u'10',
	            u'events': u'r',
	            u'fd': u'7',
	            u'flags': u'N',
	            u'idle': u'0',
	            u'multi': u'-1',
	            u'name': u'',
	            u'obl': u'0',
	            u'oll': u'0',
	            u'omem': u'0',
	            u'psub': u'0',
	            u'qbuf': u'0',
	            u'qbuf-free': u'32768',
	            u'sub': u'0'}],
	 u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.bgsave

::

	POST /BGSAVE/

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.client_getname
.. autoattribute:: lark.redis.client.RedisApiClient.client_setname
.. autoattribute:: lark.redis.client.RedisApiClient.client_kill
.. autoattribute:: lark.redis.client.RedisApiClient.config_get

::

	GET /CONFIG/GET/

	output: {u'data': {u'activerehashing': u'yes',
	           u'aof-rewrite-incremental-fsync': u'yes',
	           u'appendfsync': u'everysec',
	           u'appendonly': u'no',
	           u'auto-aof-rewrite-min-size': u'1048576',
	           u'auto-aof-rewrite-percentage': u'100',
	           u'bind': u'',
	           u'client-output-buffer-limit': u'normal 0 0 0 slave 268435456 67108864 60 pubsub 33554432 8388608 60',
	           u'daemonize': u'no',
	           u'databases': u'16',
	           u'dbfilename': u'dump.rdb',
	           u'dir': u'/Users/alex',
	           u'hash-max-ziplist-entries': u'512',
	           u'hash-max-ziplist-value': u'64',
	           u'hz': u'10',
	           u'list-max-ziplist-entries': u'512',
	           u'list-max-ziplist-value': u'64',
	           u'logfile': u'',
	           u'loglevel': u'notice',
	           u'lua-time-limit': u'5000',
	           u'masterauth': u'',
	           u'maxclients': u'10000',
	           u'maxmemory': u'0',
	           u'maxmemory-policy': u'volatile-lru',
	           u'maxmemory-samples': u'3',
	           u'min-slaves-max-lag': u'10',
	           u'min-slaves-to-write': u'0',
	           u'no-appendfsync-on-rewrite': u'no',
	           u'notify-keyspace-events': u'',
	           u'pidfile': u'/var/run/redis.pid',
	           u'port': u'6379',
	           u'rdbchecksum': u'yes',
	           u'rdbcompression': u'yes',
	           u'repl-backlog-size': u'1048576',
	           u'repl-backlog-ttl': u'3600',
	           u'repl-disable-tcp-nodelay': u'no',
	           u'repl-ping-slave-period': u'10',
	           u'repl-timeout': u'60',
	           u'requirepass': u'',
	           u'save': u'3600 1 300 100 60 10000',
	           u'set-max-intset-entries': u'512',
	           u'slave-priority': u'100',
	           u'slave-read-only': u'yes',
	           u'slave-serve-stale-data': u'yes',
	           u'slaveof': u'',
	           u'slowlog-log-slower-than': u'10000',
	           u'slowlog-max-len': u'128',
	           u'stop-writes-on-bgsave-error': u'yes',
	           u'tcp-keepalive': u'0',
	           u'timeout': u'0',
	           u'unixsocket': u'',
	           u'unixsocketperm': u'0',
	           u'watchdog-period': u'0',
	           u'zset-max-ziplist-entries': u'128',
	           u'zset-max-ziplist-value': u'64'},
	 u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.config_set

::

	POST /CONFIG/SET/maxclients/

	input: {u'value': u'9999'}

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.config_resetstat

::

	POST /CONFIG/RESETSTAT/

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.dbsize

::

	GET /DBSIZE/

	output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}

.. autoattribute:: lark.redis.client.RedisApiClient.flushall


::

	DELETE /FLUSHALL/

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.flushdb


::

	DELETE /FLUSHDB/

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lastsave


::

	GET /LASTSAVE/

	output: {u'data': u'2013-12-18T23:09:22',
	 u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.save


.. autoattribute:: lark.redis.client.RedisApiClient.debug_object
.. autoattribute:: lark.redis.client.RedisApiClient.info


::

	GET /INFO/

	output: {u'data': {u'aof_current_rewrite_time_sec': -1,
	           u'aof_enabled': 0,
	           u'aof_last_bgrewrite_status': u'ok',
	           u'aof_last_rewrite_time_sec': -1,
	           u'aof_rewrite_in_progress': 0,
	           u'aof_rewrite_scheduled': 0,
	           u'arch_bits': 64,
	           u'blocked_clients': 0,
	           u'client_biggest_input_buf': 0,
	           u'client_longest_output_list': 0,
	           u'config_file': u'',
	           u'connected_clients': 2,
	           u'connected_slaves': 0,
	           u'db0': {u'avg_ttl': 0, u'expires': 0, u'keys': 4216},
	           u'db1': {u'avg_ttl': 0, u'expires': 0, u'keys': 340806},
	           u'db2': {u'avg_ttl': 0, u'expires': 0, u'keys': 1746},
	           u'db3': {u'avg_ttl': 0, u'expires': 0, u'keys': 1},
	           u'evicted_keys': 0,
	           u'expired_keys': 0,
	           u'gcc_version': u'4.2.1',
	           u'hz': 10,
	           u'instantaneous_ops_per_sec': 0,
	           u'keyspace_hits': 216,
	           u'keyspace_misses': 26,
	           u'latest_fork_usec': 0,
	           u'loading': 0,
	           u'lru_clock': 331671,
	           u'master_repl_offset': 0,
	           u'mem_allocator': u'libc',
	           u'mem_fragmentation_ratio': 0.0,
	           u'multiplexing_api': u'kqueue',
	           u'os': u'Darwin 13.0.0 x86_64',
	           u'process_id': 55585,
	           u'pubsub_channels': 0,
	           u'pubsub_patterns': 0,
	           u'rdb_bgsave_in_progress': 0,
	           u'rdb_changes_since_last_save': 701,
	           u'rdb_current_bgsave_time_sec': -1,
	           u'rdb_last_bgsave_status': u'ok',
	           u'rdb_last_bgsave_time_sec': 2,
	           u'rdb_last_save_time': 1387436962,
	           u'redis_build_id': u'b8cc45f60db4b294',
	           u'redis_git_dirty': 0,
	           u'redis_git_sha1': 0,
	           u'redis_mode': u'standalone',
	           u'redis_version': u'2.8.1',
	           u'rejected_connections': 0,
	           u'repl_backlog_active': 0,
	           u'repl_backlog_first_byte_offset': 0,
	           u'repl_backlog_histlen': 0,
	           u'repl_backlog_size': 1048576,
	           u'role': u'master',
	           u'run_id': u'3ee0859b63dbd3a6ea41270b0f9d730d2c262af6',
	           u'sync_full': 0,
	           u'sync_partial_err': 0,
	           u'sync_partial_ok': 0,
	           u'tcp_port': 6379,
	           u'total_commands_processed': 1304,
	           u'total_connections_received': 652,
	           u'uptime_in_days': 12,
	           u'uptime_in_seconds': 1058691,
	           u'used_cpu_sys': 165.37,
	           u'used_cpu_sys_children': 100.54,
	           u'used_cpu_user': 108.23,
	           u'used_cpu_user_children': 452.6,
	           u'used_memory': 280149104,
	           u'used_memory_human': u'267.17M',
	           u'used_memory_lua': 33792,
	           u'used_memory_peak': 300950240,
	           u'used_memory_peak_human': u'287.01M',
	           u'used_memory_rss': 1179648},
	 u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.ping

::

	GET /PING/

	output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.echo

::

	POST /ECHO/

	input: {u'value': u'foo bar'}

	output: {u'data': u'foo bar', u'meta': {u'status': u'ok', u'status_code': 200}}


Key  Methods
============

.. autoattribute:: lark.redis.client.RedisApiClient.randomkey

::

  GET /RANDOMKEY/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}

.. autoattribute:: lark.redis.client.RedisApiClient.get

::

  GET /GET/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.set

::

  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.append

::

  POST /APPEND/a/

  input: {u'value': u'a1'}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.setbit

::

  POST /SETBIT/a/

  input: {u'offset': 5, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.bitcount

::

  GET /BITCOUNT/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.bitop

::

.. autoattribute:: lark.redis.client.RedisApiClient.decr

::

  POST /DECR/a/

  output: {u'data': -1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.delete

::

  DELETE /DEL/a/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.dump

.. autoattribute:: lark.redis.client.RedisApiClient.restore

.. autoattribute:: lark.redis.client.RedisApiClient.exists

::

  GET /EXISTS/a/

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.expire

::

  POST /EXPIRE/a/

  input: {u'time': 10}

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.expireat

::

  POST /EXPIREAT/a/

  input: {u'when': u'2013-12-18T23:11:39.232554'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.ttl

::

  GET /TTL/a/

  output: {u'data': 60, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.pexpire

::

  POST /PEXPIRE/a/

  input: {u'time': 60000}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.pexpireat

::

  POST /PEXPIREAT/a/

  input: {u'when': u'2013-12-18T23:11:39.681630'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.pttl

::

  GET /PTTL/a/

  output: {u'data': 996, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.psetex

::

  POST /PSETEX/a/

  input: {u'time_ms': 1000, u'value': u'value'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.persist

::

  POST /PERSIST/a/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.getbit

::

  GET /GETBIT/a/5/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.getrange

::

  GET /GETRANGE/a/0/0/

  output: {u'data': u'f', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.getset

::

  POST /GETSET/a/

  input: {u'value': u'foo'}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.incr

::

  POST /INCR/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.incrbyfloat

::

  POST /INCRBYFLOAT/a/

  output: {u'data': 1.0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.keys

::

  GET /KEYS/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.mget

::

  GET /MGET/?key=a&key=b

  output: {u'data': [None, None], u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.mset

::

  POST /MSET/

  input: [[u'a', u'1'], [u'b', u'2'], [u'c', u'3']]

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.msetnx

::

  POST /MSETNX/

  input: [[u'a', u'1'], [u'b', u'2'], [u'c', u'3']]

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.rename

::

  POST /RENAME/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.renamenx

::

  POST /RENAMENX/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.setex

::

  POST /SETEX/a/

  input: {u'time': 60, u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.setnx

::

  POST /SETNX/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.setrange

::

  POST /SETRANGE/a/

  input: {u'offset': 5, u'value': u'foo'}

  output: {u'data': 8, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.strlen

::

  GET /STRLEN/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.substr

::

  GET /SUBSTR/a/3/5/

  output: {u'data': u'345', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.type

::

  GET /TYPE/a/

  output: {u'data': u'none', u'meta': {u'status': u'ok', u'status_code': 200}}





List Methods
============

.. autoattribute:: lark.redis.client.RedisApiClient.blpop

::

  POST /BLPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'b', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.brpop

::

  POST /BRPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'b', u'4'], u'meta': {u'status': u'ok', u'status_code': 200}}

.. autoattribute:: lark.redis.client.RedisApiClient.brpoplpush

::

  POST /BRPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.lindex

::

  GET /LINDEX/a/0/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.linsert

::

  POST /LINSERT/a/

  input: {u'refvalue': u'2', u'value': u'2.5', u'where': u'after'}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.llen

::

  GET /LLEN/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lpop

::

  POST /LPOP/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lpush

::

  POST /LPUSH/a/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lpushx

::

  POST /LPUSHX/a/

  input: {u'value': u'1'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lrange

::

  GET /LRANGE/a/0/-1/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lrem

::

  DELETE /LREM/a/1/1/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.lset

::


  POST /LSET/a/

  input: {u'index': 1, u'value': u'4'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.ltrim

::

  DELETE /LTRIM/a/0/1/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.rpop

::

  POST /RPOP/a/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.rpoplpush

::

  POST /RPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': u'a3', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.rpush

::

  POST /RPUSH/a/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.rpushx

::

  POST /RPUSHX/a/

  input: {u'value': u'b'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}




Sort Method
===========

.. autoattribute:: lark.redis.client.RedisApiClient.sort

::

  GET /SORT/a/?get=user%3A%2A&get=%23&groups=1

  output: {u'data': [[u'u1', u'1'], [u'u2', u'2'], [u'u3', u'3']],
   u'meta': {u'status': u'ok', u'status_code': 200}}



Scan Method
===========

.. autoattribute:: lark.redis.client.RedisApiClient.scan

::

  GET /SCAN/?match=a

  output: {u'data': [u'0', [u'a']], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.sscan

::

  GET /SSCAN/a/?match=1

  output: {u'data': [u'0', [u'1']], u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.hscan

::

  GET /HSCAN/a/?match=a

  output: {u'data': [u'0', {u'a': u'1'}],
   u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.zscan

::

  GET /ZSCAN/a/?match=a

  output: {u'data': [u'0', [[u'a', 1.0]]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


Set Methods
===========

.. autoattribute:: lark.redis.client.RedisApiClient.sadd

::

  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.smembers

::

  GET /SMEMBERS/a/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.scard

::

  GET /SCARD/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.sdiff

::

  GET /SDIFF/?key=a&key=b

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.sdiffstore

::

  POST /SDIFFSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.sinter

::

  GET /SINTER/?key=a&key=b

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.sinterstore

::

  POST /SINTERSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.sismember

::


  GET /SISMEMBER/a/1/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.smove

::

  POST /SMOVE/

  input: {u'dst': u'b', u'src': u'a', u'value': u'a1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.spop

::

  POST /SPOP/a/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.srandmember

::

  GET /SRANDMEMBER/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.srem

::

  DELETE /SREM/a/?value=5

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.sunion

::

  GET /SUNION/?key=a&key=b

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.sunionstore

::

  POST /SUNIONSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}




Sorted Set Methods
==================

.. autoattribute:: lark.redis.client.RedisApiClient.zadd

::

  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.zcard

::

  GET /ZCARD/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zcount

::

  GET /ZCOUNT/a/-inf/+inf/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zincrby

::

  POST /ZINCRBY/a/

  input: {u'value': u'a2'}

  output: {u'data': 3.0, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.zinterstore

::

  POST /ZINTERSTORE/

  input: {u'aggregate': u'MAX', u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrange

::

  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a3', 5.0], [u'a1', 6.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrangebyscore

::


  GET /ZRANGEBYSCORE/a/2/4/?start=1&num=2

  output: {u'data': [u'a3', u'a4'], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrevrangebyscore

::

  GET /ZREVRANGEBYSCORE/a/4/2/?start=1&num=2

  output: {u'data': [u'a3', u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrank

::

  GET /ZRANK/a/a1/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrevrank

::

  GET /ZREVRANK/a/a1/

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrem

::

  DELETE /ZREM/a/?value=a2

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zremrangebyrank

::

  DELETE /ZREMRANGEBYRANK/a/1/3/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.zremrangebyscore

::

  DELETE /ZREMRANGEBYSCORE/a/2/4/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.zrevrange

::

  GET /ZREVRANGE/a/0/1/

  output: {u'data': [u'a3', u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}

.. autoattribute:: lark.redis.client.RedisApiClient.zscore

::

  GET /ZSCORE/a/a1/

  output: {u'data': 1.0, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.zunionstore

::

  POST /ZUNIONSTORE/

  input: {u'aggregate': u'MAX', u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}




Hash Methods
============

.. autoattribute:: lark.redis.client.RedisApiClient.hget

::

 GET /HGET/a/2/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hgetall

::

  GET /HGETALL/a/

  output: {u'data': {u'a1': u'1', u'a2': u'2', u'a3': u'3'},
   u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hexists

::

  GET /HEXISTS/a/1/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hdel

::

  DELETE /HDEL/a/?key=2

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hincrby

::

  POST /HINCRBY/a/1/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hincrbyfloat

::

  POST /HINCRBY/a/1/

  input: {u'amount': 2}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hkeys

::

  GET /HKEYS/a/

  output: {u'data': [u'a1', u'a3', u'a2'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hlen

::

  GET /HLEN/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hset

::

  POST /HSET/a/2/

  input: {u'value': u'5'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hsetnx

::

  POST /HSETNX/a/

  input: {u'key': u'1', u'value': u'1'}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hmset

::

  POST /HMSET/a/

  input: {u'mapping': {u'a1': u'1', u'a2': u'2', u'a3': u'3'}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}



.. autoattribute:: lark.redis.client.RedisApiClient.hmget

::

  GET /HMGET/a/?key=a&key=b&key=c

  output: {u'data': [u'1', u'2', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


.. autoattribute:: lark.redis.client.RedisApiClient.hvals

::

  GET /HVALS/a/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


