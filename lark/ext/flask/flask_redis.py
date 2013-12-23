import redis
from flask import g


class Redis(object):

    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        """
        Used to initialize redis with app object
        """

        app.config.setdefault('REDIS_URLS', {
            'main': 'redis://localhost:6379/0',
            'admin': 'redis://localhost:6379/1',
        })

        app.before_request(self.before_request)

        self.app = app

    _redis_connection = {}

    def connect(self, connection_type='main'):
        r_con = self._redis_connection.get(connection_type)
        if r_con:
            return r_con

        self._redis_connection[connection_type] = redis.Redis.from_url(self.app.config['REDIS_URLS'][connection_type])
        return self._redis_connection[connection_type]

    def before_request(self):
        g.r = self.connect()
        g.get_redis_connection = self.connect
