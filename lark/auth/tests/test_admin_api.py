from __future__ import with_statement
import json
import os
import tempfile
import unittest
import base64

from werkzeug.datastructures import Headers

from flask import Flask
from oauthlib.oauth2.rfc6749.tokens import BearerToken

from lark.auth.api import lark_admin_api
from lark.auth.models import User, Client, Token
from lark.auth.database import db


class ApiTest(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        self.db_fd, self.path = tempfile.mkstemp()
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % (self.path)
        app.register_blueprint(lark_admin_api, url_prefix='/admin')
        self.app = app
        self.client = app.test_client()
        self.request_ctx = self.app.test_request_context()
        self.request_ctx.push()
        db.create_all()
        self.client = app.test_client()

        user = User.create_user(username='test', password='test')
        self.user = user
        user2 = User.create_user(username='test2', password='test2')
        self.user2 = user2
        client = Client.create_from_user(user, {
            'name': 'Test Test',
            'description': 'test is testy',
            'redirect_uris': ['http://localhost:8000'],
        })
        self.oauth_client = client

    def tearDown(self):
        self.request_ctx.pop()
        os.close(self.db_fd)
        os.unlink(self.path)

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

    def create_access_token(self, user, oauth_client):
        class RequestValidator(object):
            def save_bearer_token(self, token, request):
                print token
                return Token.set_for_oauth2(token, request)

        validator = RequestValidator()

        bearer_token_generator = BearerToken(request_validator=validator, expires_in=3600)

        class RequestMock(object):
            scopes = ['admin']
            state = '123'
            extra_credentials = None

            def __init__(self, user, client):
                self.user = user
                self.client = client

        request = RequestMock(user=user, client=oauth_client)

        token = bearer_token_generator.create_token(request, refresh_token=True)

        return token['access_token']

    def test_client_creation(self):

        access_token = self.create_access_token(self.user, self.oauth_client)

        data = {
            'name': 'awesome sauce',
            'description': 'awesome sauce is awesome',
            'redirect_uris': ['http://localhost:4000'],
        }

        headers = Headers({
            'Authorization': 'Bearer %s' % (access_token, ),
            'Content-Type': 'application/json',
        })

        rv = self.client.post(path='/admin/clients', headers=headers, data=json.dumps(data))

        json_data = json.loads(rv.data)

        assert json_data['data']['user']['id'] == 1
        assert json_data['data']['name'] == data['name']
        assert json_data['data']['description'] == data['description']
        assert json_data['data']['redirect_uris'] == data['redirect_uris']

        rv = self.client.get(path='/admin/clients', headers=headers)
        json_data = json.loads(rv.data)
        assert len(json_data['data']) == 2

        client_id = json_data['data'][0]['client_id']
        path = '/admin/clients/%s' % (client_id)
        rv = self.client.get(path=path, headers=headers)
        json_data = json.loads(rv.data)
        assert json_data['data']['client_id'] == client_id

        client_data = json_data['data']
        client_data['name'] = 'awesome sauce 2'
        path = '/admin/clients/%s' % (client_id)
        rv = self.client.post(path=path, headers=headers, data=json.dumps(client_data))
        json_data = json.loads(rv.data)
        assert json_data['data']['client_id'] == client_id
        assert json_data['data']['name'] == 'awesome sauce 2'
