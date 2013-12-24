import base64
import json
import os
import sys

from mock import MagicMock
import redis
from unittest import TestCase


from flask import Flask
from flask_oauthlib.client import prepare_request
from .server import create_server, redis_provider
from .client import create_client

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

if sys.version_info[0] == 3:
    python_version = 3
    string_type = str
else:
    python_version = 2
    string_type = unicode

r_con = redis.Redis.from_url('redis://localhost:6379/11')

os.environ['DEBUG'] = 'true'

def u(text):
    if not isinstance(text, string_type):
        text = text.decode('utf-8')
    return text


def b(text):
    if isinstance(text, string_type):
        text = text.encode('utf-8')
    return text


def clean_url(location):
    location = u(location)
    ret = urlparse(location)
    return '%s?%s' % (ret.path, ret.query)


class OAuthSuite(TestCase):

    def setUp(self):
        app = self.create_app()

        self.setup_app(app)

        self.app = app
        self.client = app.test_client()
        return app

    def tearDown(self):
        r_con.flushall()

    def create_oauth_provider(app):
        raise NotImplementedError('Each test class must'
                                  'implement this method.')

    def create_app(self):
        app = Flask(__name__)
        app.config.update({
            'OAUTH1_PROVIDER_ENFORCE_SSL': False,
        })
        app.debug = True
        app.testing = True
        app.secret_key = 'development'
        return app

    def setup_app(self, app):
        oauth = self.create_oauth_provider(app)
        create_server(app, oauth)
        client = create_client(app)
        client.http_request = MagicMock(
            side_effect=self.patch_request(app)
        )
        return app

    def patch_request(self, app):
        test_client = app.test_client()

        def make_request(uri, headers=None, data=None, method=None):
            uri, headers, data, method = prepare_request(
                uri, headers, data, method
            )

            # test client is a `werkzeug.test.Client`
            parsed = urlparse(uri)
            uri = '%s?%s' % (parsed.path, parsed.query)
            resp = test_client.open(
                uri, headers=headers, data=data, method=method
            )
            # for compatible
            resp.code = resp.status_code
            return resp, resp.data

        return make_request

authorize_url = (
    '/oauth/authorize?response_type=code&client_id=dev'
    '&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauthorized&scope=email'
)


def _base64(text):
    return u(base64.b64encode(b(text)))


auth_code = _base64('confidential:confidential')


class TestWebAuth(OAuthSuite):

    def create_oauth_provider(self, app):
        return redis_provider(app)

    def test_login(self):
        rv = self.client.get('/login')
        assert 'response_type=code' in rv.location

    def test_oauth_authorize_invalid_url(self):
        rv = self.client.get('/oauth/authorize')
        assert 'invalid_client_id' in rv.location

    def test_oauth_authorize_valid_url(self):
        rv = self.client.get(authorize_url)
        assert b'</form>' in rv.data

        rv = self.client.post(authorize_url, data=dict(
            confirm='no'
        ))
        assert 'access_denied' in rv.location

        rv = self.client.post(authorize_url, data=dict(
            confirm='yes'
        ))
        # success
        assert 'code=' in rv.location
        assert 'state' not in rv.location

        # test state
        rv = self.client.post(authorize_url + '&state=foo', data=dict(
            confirm='yes'
        ))
        assert 'code=' in rv.location
        assert 'state' in rv.location

    def test_get_access_token(self):
        rv = self.client.post(authorize_url, data={'confirm': 'yes'})
        rv = self.client.get(clean_url(rv.location))
        assert b'access_token' in rv.data

    def test_full_flow(self):
        rv = self.client.post(authorize_url, data={'confirm': 'yes'})
        rv = self.client.get(clean_url(rv.location))
        assert b'access_token' in rv.data

        rv = self.client.get('/')
        assert b'username' in rv.data

        rv = self.client.get('/address')
        assert rv.status_code == 403

        rv = self.client.get('/method/post')
        assert b'POST' in rv.data

        rv = self.client.get('/method/put')
        assert b'PUT' in rv.data

        rv = self.client.get('/method/delete')
        assert b'DELETE' in rv.data

    def test_get_client(self):
        rv = self.client.post(authorize_url, data={'confirm': 'yes'})
        rv = self.client.get(clean_url(rv.location))
        rv = self.client.get("/client")
        assert b'dev' in rv.data

    def test_invalid_client_id(self):
        authorize_url = (
            '/oauth/authorize?response_type=code&client_id=confidential'
            '&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauthorized'
            '&scope=email'
        )
        rv = self.client.post(authorize_url, data={'confirm': 'yes'})
        rv = self.client.get(clean_url(rv.location))
        assert b'Invalid' in rv.data

    def test_invalid_response_type(self):
        authorize_url = (
            '/oauth/authorize?response_type=invalid&client_id=dev'
            '&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauthorized'
            '&scope=email'
        )
        rv = self.client.post(authorize_url, data={'confirm': 'yes'})
        rv = self.client.get(clean_url(rv.location))
        assert b'error' in rv.data


class TestPasswordAuth(OAuthSuite):

    def create_oauth_provider(self, app):
        return redis_provider(app)

    def test_get_access_token(self):
        url = ('/oauth/token?grant_type=password&state=foo'
               '&scope=email+address&username=admin&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})
        assert b'access_token' in rv.data
        assert b'state' in rv.data

    def test_invalid_user_credentials(self):
        url = ('/oauth/token?grant_type=password&state=foo'
               '&scope=email+address&username=fake&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})

        assert b'Invalid credentials given' in rv.data


class TestRefreshToken(OAuthSuite):

    def create_oauth_provider(self, app):
        return redis_provider(app)

    def test_refresh_token_in_password_grant(self):
        url = ('/oauth/token?grant_type=password'
               '&scope=email+address&username=admin&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        })
        assert b'access_token' in rv.data
        data = json.loads(u(rv.data))

        args = (data.get('scope').replace(' ', '+'),
                data.get('refresh_token'))
        url = ('/oauth/token?grant_type=refresh_token'
               '&scope=%s&refresh_token=%s&username=admin')
        url = url % args
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        })
        assert b'access_token' in rv.data


class TestCredentialAuth(OAuthSuite):

    def create_oauth_provider(self, app):
        return redis_provider(app)

    def test_get_access_token(self):
        url = ('/oauth/token?grant_type=client_credentials'
               '&scope=email+address&username=admin&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})
        assert b'access_token' in rv.data

    def test_invalid_auth_header(self):
        url = ('/oauth/token?grant_type=client_credentials'
               '&scope=email+address&username=admin&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic foobar'
        }, data={'confirm': 'yes'})
        assert b'invalid_client' in rv.data

    def test_no_client(self):
        auth_code = _base64('none:confidential')
        url = ('/oauth/token?grant_type=client_credentials'
               '&scope=email+address&username=admin&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})
        assert b'invalid_client' in rv.data

    def test_wrong_secret_client(self):
        auth_code = _base64('confidential:wrong')
        url = ('/oauth/token?grant_type=client_credentials'
               '&scope=email+address&username=admin&password=admin')
        rv = self.client.get(url, headers={
            'Authorization': 'Basic %s' % auth_code,
        }, data={'confirm': 'yes'})
        assert b'invalid_client' in rv.data


class TestTokenGenerator(OAuthSuite):

    def create_oauth_provider(self, app):

        def generator(request, refresh_token=False):
            return 'foobar'

        app.config['OAUTH2_PROVIDER_TOKEN_GENERATOR'] = generator
        return redis_provider(app)

    def test_get_access_token(self):
        rv = self.client.post(authorize_url, data={'confirm': 'yes'})
        rv = self.client.get(clean_url(rv.location))
        data = json.loads(u(rv.data))
        assert data['access_token'] == 'foobar'
        assert data['refresh_token'] == 'foobar'
