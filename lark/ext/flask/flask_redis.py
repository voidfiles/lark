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
        app.config.setdefault('REDIS_URL', 'redis://localhost:6379/0')
        app.before_request(self.before_request)

        self.app = app

    _redis_connection = None

    def connect(self):
        if self._redis_connection:
            return self._redis_connection

        self._redis_connection = redis.Redis.from_url(self.app.config['REDIS_URL'])
        return self._redis_connection

    def before_request(self):
        g.r = self.connect()
