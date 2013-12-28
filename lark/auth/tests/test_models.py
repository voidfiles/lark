from datetime import datetime, timedelta
import os
import tempfile
import unittest

from flask import Flask

from lark.auth.models import User, Client, Grant, Token
from lark.auth.api import lark_admin_api
from lark.auth.database import db


class ModelTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        self.db_fd, self.path = tempfile.mkstemp()
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % (self.path)
        app.register_blueprint(lark_admin_api, url_prefix='/admin')
        self.app = app
        self.request_ctx = self.app.test_request_context()
        self.request_ctx.push()
        db.create_all()

    def tearDown(self):
        self.request_ctx.pop()
        os.close(self.db_fd)
        os.unlink(self.path)

    def create_user(self, username='voidfiles', password='awesome', external_access_token='abc', remote_user_id=3):
        user_data = {
            'username': username,
            'password': password,
            'external_access_token': external_access_token,
            'remote_user_id': remote_user_id,
        }

        user = User.create_user(**user_data)
        db.session.add(user)
        db.session.commit()

        return user

    def test_user(self):
        user = self.create_user()

        assert User.get_for_oauth2('voidfiles', 'awesome', {}, {}).id == user.id

    def create_client(self, user, name='TextApp', description='An awesome test app', client_id='123', client_secret='abc',
                      is_confidential=True, default_scope=['email', 'user'],
                      redirect_uris=['http://example.com', 'http://example.com/2']):

        client_data = {
            'user': user,
            'name': name,
            'description': description,
            'client_id': client_id,
            'client_secret': client_secret,
            '_default_scopes': ' '.join(default_scope),
            '_redirect_uris': ' '.join(redirect_uris),
        }

        client = Client(**client_data)
        db.session.add(client)
        db.session.commit()

        return client

    def test_client(self):
        user = self.create_user()

        client = self.create_client(user)

        assert client.user.id == user.id
        assert client.redirect_uris == ['http://example.com', 'http://example.com/2']
        assert client.default_scopes == ['email', 'user']
        assert client.default_redirect_uri == 'http://example.com'
        assert Client.get_for_oauth2('123').client_id == client.client_id

    def test_grant(self):
        user = self.create_user()
        client = self.create_client(user)
        print user
        print client
        data = {
            'user_id': user.id,
            'user': user,
            'client': client,
            'client_id': client.client_id,
            'code': '101112',
            'redirect_uri': 'http://example.com',
            '_scopes': 'email user',
            'expires': datetime.utcnow() + timedelta(seconds=10),
        }

        grant = Grant(**data)
        db.session.add(grant)
        db.session.commit()
        grant = Grant.get_for_oauth2(client.client_id, '101112')
        assert grant.user.id == user.id
        assert grant.client_id == client.client_id
        assert grant.scopes == ['email', 'user']
        assert Grant.get_for_oauth2(client.client_id, '101112').id == grant.id

        class Request(object):
            scopes = ['email', 'user']
            redirect_uri = 'http://example.com'

            def __init__(self, user):
                self.user = user

        request = Request(user=user)
        current_user = lambda: request.user
        grant = Grant.set_for_oauth2(current_user, 'abcdef', {'code': '123'}, request)

        assert grant.scopes == ['email', 'user']
        assert grant.client_id == 'abcdef'
        assert grant.code == '123'

    def test_token(self):
        user = self.create_user()
        client = self.create_client(user)

        token_data = {
            'user': user,
            'client': client,
            'token_type': 'bearer',
            'access_token': '123',
            'refresh_token': 'abc',
            'expires': datetime.utcnow() + timedelta(seconds=3600),
            '_scopes': 'email user',
        }

        token = Token(**token_data)
        db.session.add(token)
        db.session.commit()

        token = Token.get_for_oauth2(access_token='123')

        assert token.user.id == user.id
        assert token.client.client_id == client.client_id
        assert token.scopes == ['email', 'user']

        class Request(object):
            scopes = ['email', 'user']

            def __init__(self, user, client):
                self.user = user
                self.client = client

        request = Request(user=user, client=client)

        token_data = {
            'expires_in': 3600,
            'access_token': 'abc',
            'refresh_token': '123',
            'token_type': 'Bearer',
            'scope': ['email', 'user'],
        }

        token = Token.set_for_oauth2(token_data, request)
        assert token.user.id == user.id
        assert token.client.client_id == client.client_id
        assert token.scopes == ['email', 'user']

        token = Token.get_for_oauth2(access_token='abc')
        assert token.user.id == user.id
        assert token.client.client_id == client.client_id
        assert token.scopes == ['email', 'user']

        token = Token.get_for_oauth2(refresh_token='123')
        assert token.user.id == user.id
        assert token.client.client_id == client.client_id
        assert token.scopes == ['email', 'user']


if __name__ == '__main__':
    unittest.main()
