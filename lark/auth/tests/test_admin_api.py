from __future__ import with_statement
import binascii
import datetime
import json
import pprint
import os
import time
import unittest
import base64
from urllib import urlencode

from flask import Flask

from lark.auth.api import lark_admin_api
from lark.auth.models import User, Client
import redis

from .server import redis_provider

app = Flask(__name__)
app.config['REDIS_URLS'] = {
    'main': 'redis://localhost:6379/10',
    'admin': 'redis://localhost:6379/11',
}
app.config['DEBUG'] = True

r_con = redis.Redis.from_url('redis://localhost:6379/11')

app.register_blueprint(lark_admin_api, url_prefix='/admin')


class ApiTest(unittest.TestCase):

    def setUp(self):
        user = User(r_con, username='test', password='test')
        user.save()
        self.user = user
        client = Client.create_from_user(r_con, user, {
            'name': 'Test Test',
            'description': 'test is testy',
            'redirect_uris': ['http://localhost:8000'],
        })
        self.oauth_client = client
        self.client = app.test_client()

    def tearDown(self):
        r_con.flushall()

    ### SERVER INFORMATION ###
    def test_get_access_token(self):
        url = ('/admin/oauth/token?grant_type=password&state=foo'
               '&scope=email+address&username=test&password=test')

        auth_code = '%s:%s' % (self.oauth_client.client_id, self.oauth_client.client_secret)
        auth_code = base64.b64encode(auth_code)

        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})
        print rv.data
        assert b'access_token' in rv.data
        assert b'state' in rv.data
