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
from oauthlib.oauth2.rfc6749.tokens import BearerToken

from lark.auth.api import lark_admin_api
from lark.auth.models import User, Client, Token
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

app.config.setdefault('REDIS_URLS', {
    'main': 'redis://localhost:6379/10',
    'admin': 'redis://localhost:6379/11',
})


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
               '&scope=admin&username=test&password=test')

        auth_code = '%s:%s' % (self.oauth_client.client_id, self.oauth_client.client_secret)
        auth_code = base64.b64encode(auth_code)

        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})

        resp_json = json.loads(rv.data)
        assert 'access_token' in resp_json
        assert 'state' in resp_json

        data = {
            'name': 'awesome sauce',
            'description': 'awesome sauce is awesome',
            'redirect_uris': ['http://localhost:4000'],
        }

        rv = self.client.post('/admin/clients', headers={
            'Authorization': 'Bearer %s' % (resp_json['access_token'], ),
            'Content-Type': 'application/json',
        }, data=json.dumps(data))

        json_data = json.loads(rv.data)

        assert json_data['data']['user']['id'] == 1

    def test_client_creation(self):

        class RequestValidator(object):
            def save_bearer_token(self, token, request):
                return Token.set_for_oauth2(r_con, token, request)

        validator = RequestValidator()

        bearer_token_generator = BearerToken(request_validator=validator, expires_in=3600)

        class RequestMock(object):
            scopes = ['admin']
            state = '123'
            extra_credentials = None

            def __init__(self, user, client):
                self.user = user
                self.client = client

        request = RequestMock(user=self.user, client=self.oauth_client)

        token = bearer_token_generator.create_token(request, refresh_token=True)

        access_token = token['access_token']

        data = {
            'name': 'awesome sauce',
            'description': 'awesome sauce is awesome',
            'redirect_uris': ['http://localhost:4000'],
        }

        rv = self.client.post('/admin/clients', headers={
            'Authorization': 'Bearer %s' % (access_token, ),
            'Content-Type': 'application/json',
        }, data=json.dumps(data))

        json_data = json.loads(rv.data)

        assert json_data['data']['user']['id'] == 1
        assert json_data['data']['name'] == data['name']
        assert json_data['data']['description'] == data['description']
        assert json_data['data']['redirect_uris'] == data['redirect_uris']
