  ***********************
  Redis API HTTP Commands
  ***********************

  These will change depending on how you mount the adapater in your URL configuration, and how you decide to adapt the HTTP requests, but these are examples of how you could make API calls


  FLUSHDB
  _______

  redis docs `flushdb <http://redis.io/commands/flushdb>`_.



  POST /APPEND/a/

  input: {u'value': u'a1'}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'a1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /APPEND/a/

  input: {u'value': u'a2'}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'a1a2', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 5, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 6, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 5, u'value': False}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 9, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 17, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 25, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 33, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/0/-1/

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/2/3/

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/2/-1/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/-2/-1/

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /BITCOUNT/a/1/1/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/b/

  input: {u'values': [u'3', u'4']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BLPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'b', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BLPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'b', u'4'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BLPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'a', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BLPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'a', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BLPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/c/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BLPOP/

  input: {u'keys': [u'c'], u'timeout': 1}

  output: {u'data': [u'c', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/b/

  input: {u'values': [u'3', u'4']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'b', u'4'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'b', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'a', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': [u'a', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOP/

  input: {u'keys': [u'b', u'a'], u'timeout': 1}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/c/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOP/

  input: {u'keys': [u'c'], u'timeout': 1}

  output: {u'data': [u'c', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/b/

  input: {u'values': [u'3', u'4']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a', u'timeout': 1}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/b/0/-1/

  output: {u'data': [u'1', u'2', u'3', u'4'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /BRPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': u'', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /PING/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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
             u'keyspace_hits': 0,
             u'keyspace_misses': 0,
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
             u'total_commands_processed': 2,
             u'total_connections_received': 1,
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


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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


  POST /CONFIG/SET/maxclients/

  input: {u'value': u'9999'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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
             u'maxclients': u'9999',
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


  POST /CONFIG/SET/maxclients/

  input: {u'value': u'10000'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'bar'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /DECR/a/

  output: {u'data': -1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'-1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /DECR/a/

  output: {u'data': -2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'-2', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /DECRBY/a/

  input: {u'amount': u'5'}

  output: {u'data': -7, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'-7', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /DEL/a/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /DEL/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'bar'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /DEL/?name=a&name=b

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/b/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}





  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /EXISTS/a/

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /EXPIRE/a/

  input: {u'time': 10}

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /EXPIRE/a/

  input: {u'time': 10}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': 10, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /PERSIST/a/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /EXPIREAT/a/

  input: {u'when': u'2013-12-18T23:11:39.232554'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': 60, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /EXPIREAT/a/

  input: {u'when': u'2013-12-18T23:11:39.242542'}

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/byte_string/

  input: {u'value': u'value'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/integer/

  input: {u'value': u'5'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/byte_string/

  output: {u'data': u'value', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/integer/

  output: {u'data': u'5', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETBIT/a/5/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 5, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETBIT/a/5/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 4, u'value': False}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETBIT/a/4/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 4, u'value': True}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETBIT/a/4/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETBIT/a/

  input: {u'offset': 5, u'value': True}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETBIT/a/5/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETRANGE/a/0/0/

  output: {u'data': u'f', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETRANGE/a/0/2/

  output: {u'data': u'foo', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GETRANGE/a/3/4/

  output: {u'data': u'', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /GETSET/a/

  input: {u'value': u'foo'}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /GETSET/a/

  input: {u'value': u'bar'}

  output: {u'data': u'foo', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'1': 1, u'2': 2, u'3': 3}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /HDEL/a/?key=2

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/2/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /HDEL/a/?key=1&key=3

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HLEN/a/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'1': 1, u'2': 2, u'3': 3}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HEXISTS/a/1/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HEXISTS/a/4/

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'1': 1, u'2': 2, u'3': 3}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/1/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/2/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/3/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HSET/a/2/

  input: {u'value': u'5'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/2/

  output: {u'data': u'5', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HSET/a/4/

  input: {u'value': u'4'}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/4/

  output: {u'data': u'4', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/b/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'a1': u'1', u'a2': u'2', u'a3': u'3'}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGETALL/a/

  output: {u'data': {u'a1': u'1', u'a2': u'2', u'a3': u'3'},
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HINCRBY/a/1/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HINCRBY/a/1/

  input: {u'amount': 2}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HINCRBY/a/1/

  input: {u'amount': -2}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HINCRBYFLOAT/a/1/

  output: {u'data': 1.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HINCRBYFLOAT/a/1/

  output: {u'data': 2.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HINCRBYFLOAT/a/1/

  input: {u'amount': 1.2}

  output: {u'data': 3.2, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'a1': u'1', u'a2': u'2', u'a3': u'3'}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HKEYS/a/

  output: {u'data': [u'a1', u'a3', u'a2'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'1': 1, u'2': 2, u'3': 3}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HLEN/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'a': 1, u'b': 2, u'c': 3}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HMGET/a/?key=a&key=b&key=c

  output: {u'data': [u'1', u'2', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'a': u'1', u'b': u'2', u'c': u'3'}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGETALL/a/

  output: {u'data': {u'a': u'1', u'b': u'2', u'c': u'3'},
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'a': 1, u'b': 2, u'c': 3}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HSCAN/a/

  output: {u'data': [u'0', {u'a': u'1', u'b': u'2', u'c': u'3'}],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HSCAN/a/?match=a

  output: {u'data': [u'0', {u'a': u'1'}],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HSETNX/a/

  input: {u'key': u'1', u'value': u'1'}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/1/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HSETNX/a/

  input: {u'key': u'1', u'value': u'2'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HGET/a/1/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /HMSET/a/

  input: {u'mapping': {u'a1': u'1', u'a2': u'2', u'a3': u'3'}}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /HVALS/a/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCR/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCR/a/

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCRBY/a/

  input: {u'amount': u'5'}

  output: {u'data': 7, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'7', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCRBY/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCRBY/a/

  input: {u'amount': 4}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'5', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCRBYFLOAT/a/

  output: {u'data': 1.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /INCRBYFLOAT/a/

  input: {u'amount': 1.1}

  output: {u'data': 2.1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'2.1', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'bar'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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
             u'db10': {u'avg_ttl': 0, u'expires': 0, u'keys': 2},
             u'db2': {u'avg_ttl': 0, u'expires': 0, u'keys': 1746},
             u'db3': {u'avg_ttl': 0, u'expires': 0, u'keys': 1},
             u'evicted_keys': 0,
             u'expired_keys': 0,
             u'gcc_version': u'4.2.1',
             u'hz': 10,
             u'instantaneous_ops_per_sec': -665,
             u'keyspace_hits': 43,
             u'keyspace_misses': 8,
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
             u'rdb_changes_since_last_save': 784,
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
             u'total_commands_processed': 288,
             u'total_connections_received': 144,
             u'uptime_in_days': 12,
             u'uptime_in_seconds': 1058691,
             u'used_cpu_sys': 165.38,
             u'used_cpu_sys_children': 100.54,
             u'used_cpu_user': 108.24,
             u'used_cpu_user_children': 452.6,
             u'used_memory': 280149296,
             u'used_memory_human': u'267.17M',
             u'used_memory_lua': 33792,
             u'used_memory_peak': 300950240,
             u'used_memory_peak_human': u'287.01M',
             u'used_memory_rss': 1187840},
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /KEYS/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/testc/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/test_b/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/test_a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /KEYS/test_*/

  output: {u'data': [u'test_b', u'test_a'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /KEYS/test*/

  output: {u'data': [u'test_b', u'testc', u'test_a'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}





  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LINDEX/a/0/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LINDEX/a/1/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LINDEX/a/2/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LINSERT/a/

  input: {u'refvalue': u'2', u'value': u'2.5', u'where': u'after'}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'2', u'2.5', u'3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LINSERT/a/

  input: {u'refvalue': u'2', u'value': u'1.5', u'where': u'before'}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'1.5', u'2', u'2.5', u'3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LLEN/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPOP/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPOP/a/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPOP/a/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPOP/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPUSH/a/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPUSH/a/

  input: {u'values': [u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPUSH/a/

  input: {u'values': [u'3', u'4']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'4', u'3', u'2', u'1'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPUSHX/a/

  input: {u'value': u'1'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPUSHX/a/

  input: {u'value': u'4'}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'4', u'1', u'2', u'3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3', u'4', u'5']}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/2/

  output: {u'data': [u'1', u'2', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/2/10/

  output: {u'data': [u'3', u'4', u'5'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'2', u'3', u'4', u'5'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'1', u'1', u'1']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /LREM/a/1/1/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'1', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /LREM/a/1/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'2', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LSET/a/

  input: {u'index': 1, u'value': u'4'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/2/

  output: {u'data': [u'1', u'4', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /LTRIM/a/0/1/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /MGET/?key=a&key=b

  output: {u'data': [None, None], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/c/

  input: {u'value': u'3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /MGET/?key=a&key=other&key=b&key=c

  output: {u'data': [u'1', None, u'2', u'3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /MSET/

  input: [[u'a', u'1'], [u'b', u'2'], [u'c', u'3']]

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/b/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/c/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /MSETNX/

  input: [[u'a', u'1'], [u'b', u'2'], [u'c', u'3']]

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /MSETNX/

  input: [[u'a', u'x'], [u'd', u'4']]

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/b/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/c/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/d/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /PEXPIRE/a/

  input: {u'time': 60000}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /PEXPIRE/a/

  input: {u'time': 60000}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /PTTL/a/

  output: {u'data': 59997, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /PERSIST/a/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /PTTL/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /PEXPIREAT/a/

  input: {u'when': u'2013-12-18T23:11:39.681630'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}





  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /PSETEX/a/

  input: {u'time_ms': 1000, u'value': u'value'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'value', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /PTTL/a/

  output: {u'data': 996, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /RANDOMKEY/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/c/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /RANDOMKEY/

  output: {u'data': u'b', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RENAME/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/b/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RENAMENX/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/b/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPOP/a/

  output: {u'data': u'3', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPOP/a/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPOP/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPOP/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'a1', u'a2', u'a3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/b/

  input: {u'values': [u'b1', u'b2', u'b3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPOPLPUSH/

  input: {u'dst': u'b', u'src': u'a'}

  output: {u'data': u'a3', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'a1', u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/b/0/-1/

  output: {u'data': [u'a3', u'b1', u'b2', u'b3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'3', u'4']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'2', u'3', u'4'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSHX/a/

  input: {u'value': u'b'}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSHX/a/

  input: {u'value': u'4'}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/a/0/-1/

  output: {u'data': [u'1', u'2', u'3', u'4'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/a/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/b/

  input: {u'value': u'2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/c/

  input: {u'value': u'3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SCAN/

  output: {u'data': [u'0', [u'c', u'b', u'a']],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SCAN/?match=a

  output: {u'data': [u'0', [u'a']], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SCARD/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


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
             {u'addr': u'127.0.0.1:51981',
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


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SDIFF/?key=a&key=b

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'2', u'3']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SDIFF/?key=a&key=b

  output: {u'data': [u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SDIFFSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/c/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'2', u'3']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SDIFFSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/c/

  output: {u'data': [u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'ex': 10, u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': 10, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'px': 10000, u'value': u'1', u'xx': True}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': 10, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'nx': True, u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'nx': True, u'value': u'2'}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'px': 10000, u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /PTTL/a/

  output: {u'data': 9995, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': 10, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1', u'xx': True}

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'bar'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'2', u'xx': True}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETEX/a/

  input: {u'time': 60, u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TTL/a/

  output: {u'data': 60, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETNX/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETNX/a/

  input: {u'value': u'2'}

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETRANGE/a/

  input: {u'offset': 5, u'value': u'foo'}

  output: {u'data': 8, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'\x00\x00\x00\x00\x00foo',
   u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'abcdefghijh'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SETRANGE/a/

  input: {u'offset': 6, u'value': u'12345'}

  output: {u'data': 11, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /GET/a/

  output: {u'data': u'abcdef12345', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SINTER/?key=a&key=b

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'2', u'3']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SINTER/?key=a&key=b

  output: {u'data': [u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SINTERSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/c/

  output: {u'data': [], u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'2', u'3']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SINTERSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/c/

  output: {u'data': [u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SISMEMBER/a/1/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SISMEMBER/a/2/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SISMEMBER/a/3/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SISMEMBER/a/4/

  output: {u'data': False, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/a/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'a1', u'a2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'b1', u'b2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SMOVE/

  input: {u'dst': u'b', u'src': u'a', u'value': u'a1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/a/

  output: {u'data': [u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/b/

  output: {u'data': [u'a1', u'b1', u'b2'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'e', u'c', u'b', u'd', u'a']}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?alpha=1

  output: {u'data': [u'a', u'b', u'c', u'd', u'e'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'3', u'2', u'1', u'4']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/

  output: {u'data': [u'1', u'2', u'3', u'4'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/score:1/

  input: {u'value': u'8'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/score:2/

  input: {u'value': u'3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/score:3/

  input: {u'value': u'5'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'3', u'2', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?by=score%3A%2A

  output: {u'data': [u'2', u'3', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2', u'3', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?desc=1

  output: {u'data': [u'3', u'2', u'1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:1/

  input: {u'value': u'u1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:2/

  input: {u'value': u'u2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:3/

  input: {u'value': u'u3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2', u'3', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?get=user%3A%2A

  output: {u'data': [u'u1', u'u2', u'u3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:1/

  input: {u'value': u'u1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:2/

  input: {u'value': u'u2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:3/

  input: {u'value': u'u3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2', u'3', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?get=user%3A%2A&get=%23&groups=1

  output: {u'data': [[u'u1', u'1'], [u'u2', u'2'], [u'u3', u'3']],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:1/

  input: {u'value': u'u1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:2/

  input: {u'value': u'u2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:3/

  input: {u'value': u'u3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2', u'3', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?get=user%3A%2A&get=%23

  output: {u'data': [u'u1', u'1', u'u2', u'2', u'u3', u'3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:1/

  input: {u'value': u'u1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:2/

  input: {u'value': u'u2'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/user:3/

  input: {u'value': u'u3'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2', u'3', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?get=user%3A%2A&groups=1

  output: {u'meta': {u'error_message': u'when using "groups" the "get" argument must be specified and contain at least two keys',
             u'status': u'error',
             u'status_code': 400}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'3', u'2', u'1', u'4']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?start=1&num=2

  output: {u'data': [u'2', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /RPUSH/a/

  input: {u'values': [u'2', u'3', u'1']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SORT/a/?store=sorted_values

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /LRANGE/sorted_values/0/-1/

  output: {u'data': [u'1', u'2', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SPOP/a/

  output: {u'data': u'2', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/a/

  output: {u'data': [u'1', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SRANDMEMBER/a/

  output: {u'data': u'1', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SRANDMEMBER/a/2/

  output: {u'data': [u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2', u'3', u'4']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /SREM/a/?value=5

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /SREM/a/?value=2&value=4

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/a/

  output: {u'data': [u'1', u'3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [1, 2, 3]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SSCAN/a/

  output: {u'data': [u'0', [u'1', u'2', u'3']],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SSCAN/a/?match=1

  output: {u'data': [u'0', [u'1']], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'foo'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /STRLEN/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'0123456789'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SUBSTR/a/0/

  output: {u'data': u'0123456789', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SUBSTR/a/2/

  output: {u'data': u'23456789', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SUBSTR/a/3/5/

  output: {u'data': u'345', u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SUBSTR/a/3/-2/

  output: {u'data': u'345678', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'2', u'3']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SUNION/?key=a&key=b

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1', u'2']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/b/

  input: {u'values': [u'2', u'3']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SUNIONSTORE/

  input: {u'dest': u'c', u'keys': [u'a', u'b']}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /SMEMBERS/c/

  output: {u'data': [u'1', u'3', u'2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TYPE/a/

  output: {u'data': u'none', u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SET/a/

  input: {u'value': u'1'}

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TYPE/a/

  output: {u'data': u'string', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /DEL/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /LPUSH/a/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TYPE/a/

  output: {u'data': u'list', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /DEL/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /SADD/a/

  input: {u'values': [u'1']}

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TYPE/a/

  output: {u'data': u'set', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /DEL/a/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /TYPE/a/

  output: {u'data': u'zset', u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/-1/

  output: {u'data': [u'a1', u'a2', u'a3'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZCARD/a/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZCOUNT/a/-inf/+inf/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZCOUNT/a/1/2/

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZCOUNT/a/10/20/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZINCRBY/a/

  input: {u'value': u'a2'}

  output: {u'data': 3.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZINCRBY/a/

  input: {u'amount': 5, u'value': u'a3'}

  output: {u'data': 8.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCORE/a/a2/

  output: {u'data': 3.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCORE/a/a3/

  output: {u'data': 8.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 1], [u'a3', 1]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 2]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZINTERSTORE/

  input: {u'aggregate': u'MAX', u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a3', 5.0], [u'a1', 6.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 3], [u'a3', 5]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZINTERSTORE/

  input: {u'aggregate': u'MIN', u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a1', 1.0], [u'a3', 3.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 1], [u'a3', 1]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 2]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZINTERSTORE/

  input: {u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a3', 8.0], [u'a1', 9.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 1], [u'a3', 1]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 2]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZINTERSTORE/

  input: {u'dest': u'd', u'keys': {u'a': 1, u'b': 2, u'c': 3}}

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a3', 20.0], [u'a1', 23.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/1/

  output: {u'data': [u'a1', u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/1/2/

  output: {u'data': [u'a2', u'a3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/1/?withscores=1

  output: {u'data': [[u'a1', 1.0], [u'a2', 2.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/1/2/?withscores=1

  output: {u'data': [[u'a2', 2.0], [u'a3', 3.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/1/?withscores=1&score_cast_func=int

  output: {u'data': [[u'a1', 1], [u'a2', 2]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3], [u'a4', 4], [u'a5', 5]]}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGEBYSCORE/a/2/4/

  output: {u'data': [u'a2', u'a3', u'a4'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGEBYSCORE/a/2/4/?start=1&num=2

  output: {u'data': [u'a3', u'a4'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGEBYSCORE/a/2/4/?withscores=1

  output: {u'data': [[u'a2', 2.0], [u'a3', 3.0], [u'a4', 4.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGEBYSCORE/a/2/4/?withscores=1&score_cast_func=int

  output: {u'data': [[u'a2', 2], [u'a3', 3], [u'a4', 4]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3], [u'a4', 4], [u'a5', 5]]}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANK/a/a1/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANK/a/a2/

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANK/a/a6/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /ZREM/a/?value=a2

  output: {u'data': 1, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/-1/

  output: {u'data': [u'a1', u'a3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /ZREM/a/?value=b

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/-1/

  output: {u'data': [u'a1', u'a3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /ZREM/a/?value=a1&value=a2

  output: {u'data': 2, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/5/

  output: {u'data': [u'a3'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3], [u'a4', 4], [u'a5', 5]]}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /ZREMRANGEBYRANK/a/1/3/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/5/

  output: {u'data': [u'a1', u'a5'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3], [u'a4', 4], [u'a5', 5]]}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /ZREMRANGEBYSCORE/a/2/4/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/-1/

  output: {u'data': [u'a1', u'a5'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /ZREMRANGEBYSCORE/a/2/4/

  output: {u'data': 0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/a/0/-1/

  output: {u'data': [u'a1', u'a5'], u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGE/a/0/1/

  output: {u'data': [u'a3', u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGE/a/1/2/

  output: {u'data': [u'a2', u'a1'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGE/a/0/1/?withscores=1

  output: {u'data': [[u'a3', 3.0], [u'a2', 2.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGE/a/1/2/?withscores=1

  output: {u'data': [[u'a2', 2.0], [u'a1', 1.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGE/a/0/1/?withscores=1&score_cast_func=int

  output: {u'data': [[u'a3', 3], [u'a2', 2]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3], [u'a4', 4], [u'a5', 5]]}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGEBYSCORE/a/4/2/

  output: {u'data': [u'a4', u'a3', u'a2'],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGEBYSCORE/a/4/2/?start=1&num=2

  output: {u'data': [u'a3', u'a2'], u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGEBYSCORE/a/4/2/?withscores=1

  output: {u'data': [[u'a4', 4.0], [u'a3', 3.0], [u'a2', 2.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANGEBYSCORE/a/4/2/?withscores=1&score_cast_func=int

  output: {u'data': [[u'a4', 4], [u'a3', 3], [u'a2', 2]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3], [u'a4', 4], [u'a5', 5]]}

  output: {u'data': 5, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANK/a/a1/

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANK/a/a2/

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZREVRANK/a/a6/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a', 1], [u'b', 2], [u'c', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCAN/a/

  output: {u'data': [u'0', [[u'a', 1.0], [u'b', 2.0], [u'c', 3.0]]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCAN/a/?match=a

  output: {u'data': [u'0', [[u'a', 1.0]]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCORE/a/a1/

  output: {u'data': 1.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCORE/a/a2/

  output: {u'data': 2.0, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZSCORE/a/a4/

  output: {u'data': None, u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 1], [u'a3', 1]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 2]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZUNIONSTORE/

  input: {u'aggregate': u'MAX', u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a2', 2.0], [u'a4', 4.0], [u'a3', 5.0], [u'a1', 6.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 2], [u'a3', 3]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZUNIONSTORE/

  input: {u'aggregate': u'MIN', u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a1', 1.0], [u'a2', 2.0], [u'a3', 3.0], [u'a4', 4.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 1], [u'a3', 1]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 2]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZUNIONSTORE/

  input: {u'dest': u'd', u'keys': [u'a', u'b', u'c']}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a2', 3.0], [u'a4', 4.0], [u'a3', 8.0], [u'a1', 9.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/a/

  input: {u'scores': [[u'a1', 1], [u'a2', 1], [u'a3', 1]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/b/

  input: {u'scores': [[u'a1', 2], [u'a2', 2], [u'a3', 2]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZADD/c/

  input: {u'scores': [[u'a1', 6], [u'a3', 5], [u'a4', 4]]}

  output: {u'data': 3, u'meta': {u'status': u'ok', u'status_code': 200}}


  POST /ZUNIONSTORE/

  input: {u'dest': u'd', u'keys': {u'a': 1, u'b': 2, u'c': 3}}

  output: {u'data': 4, u'meta': {u'status': u'ok', u'status_code': 200}}


  GET /ZRANGE/d/0/-1/?withscores=1

  output: {u'data': [[u'a2', 5.0], [u'a4', 12.0], [u'a3', 20.0], [u'a1', 23.0]],
   u'meta': {u'status': u'ok', u'status_code': 200}}


  DELETE /FLUSHDB/

  output: {u'data': True, u'meta': {u'status': u'ok', u'status_code': 200}}
