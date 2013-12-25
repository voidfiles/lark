from datetime import datetime, timedelta
import redis
from lark.auth.models import StuctRedisModel, User, Client, Grant, Token
import unittest

r_con = redis.Redis.from_url('redis://localhost:6379/11')


class ModelTests(unittest.TestCase):

    def tearDown(self):
        r_con.flushall()

    def create_user(self, username='voidfiles', password='awesome', external_access_token='abc', remote_user_id=3):
        user_data = {
            'username': username,
            'password': password,
            'external_access_token': external_access_token,
            'remote_user_id': remote_user_id,
        }

        user = User(r_con, **user_data)

        user.save()

        return user

    def test_base(self):

        class TestModel(StuctRedisModel):
            key_prefix = 'test'

            valid_attrs = (
                'pk',
                'attr',
                'fk',
            )

            indexes = (
                'attr',
                'custom_index',
            )

            list_indexes = (
                'fk',
            )

            @property
            def custom_index(self):
                return '%s:b' % (self.attr)

        model_data = {
            'attr': 'awesome',
            'fk': 1,
        }

        model_data_with_extra = {
            'non_attr': 'not_cool'
        }

        model_data_with_extra.update(model_data)

        test_model = TestModel(r_con, **model_data_with_extra)

        assert test_model.attr == 'awesome'
        assert not hasattr(test_model, 'not_cool')

        model_data = {
            'pk': None,
            'attr': 'awesome',
            'fk': 1,
        }
        test_model = TestModel(r_con, **model_data)

        assert test_model.to_dict() == model_data

        assert test_model.serialize() == '{"pk": null, "fk": 1, "attr": "awesome"}'
        test_model.save()

        assert r_con.get('test:1') == '{"pk": 1, "fk": 1, "attr": "awesome"}'
        assert r_con.get('test:attr:awesome') == '1'

        assert TestModel.by_pk(r_con, 1).attr == 'awesome'
        assert TestModel.get_by_index(r_con, 'attr', 'awesome').attr == 'awesome'
        assert TestModel.get_by_index(r_con, 'custom_index', 'awesome:b').attr == 'awesome'

        test_model.delete()

        assert r_con.get('test:1') is None
        assert r_con.get('test:attr:awesome') is None

        model_data_1 = {
            'pk': None,
            'attr': 'awesome',
            'fk': 1,
        }

        model_data_2 = {
            'pk': None,
            'attr': 'awesome2',
            'fk': 1,
        }

        test_model1 = TestModel(r_con, **model_data_1)
        test_model1.save()
        test_model2 = TestModel(r_con, **model_data_2)
        test_model2.save()

        test_models = TestModel.by_pks(r_con, [test_model1.pk, test_model2.pk])
        assert len(test_models) == 2
        test_models = TestModel.get_list_by_index(r_con, 'fk', 1)
        assert len(test_models) == 2

    def test_user(self):
        user = self.create_user()

        assert User.get_for_oauth2(r_con, 'voidfiles', 'awesome', {}, {}).pk == user.pk

    def create_client(self, user, name='TextApp', description='An awesome test app', client_id='123', client_secret='abc',
                      client_type='normal', default_scope=['email', 'user'],
                      redirect_uris=['http://example.com', 'http://example.com/2']):

        client_data = {
            'user': user,
            'name': name,
            'description': description,
            'client_id': client_id,
            'client_secret': client_secret,
            'client_type': client_type,
            'default_scope': default_scope,
            'redirect_uris': redirect_uris,
        }

        client = Client(r_con, **client_data)

        client.save()

        return client

    def test_client(self):
        user = self.create_user()

        client = self.create_client(user)

        assert client.user.pk == user.pk
        assert client.redirect_uris == ['http://example.com', 'http://example.com/2']
        assert client.default_scopes == ['email', 'user']
        assert client.default_redirect_uri == 'http://example.com'
        assert Client.get_for_oauth2(r_con, '123').pk == client.pk

    def test_grant(self):
        user = self.create_user()
        client = self.create_client(user)

        data = {
            'user': user,
            'client_id': client.client_id,
            'code': '101112',
            'redirect_uri': 'http://example.com',
            'scope': ['email', 'user'],
            'expires': datetime.utcnow() + timedelta(seconds=10),
            'allowed_grant_types': ['client_credentials', 'bearer'],
            'allowed_response_types': ['a', 'b'],
        }

        grant = Grant(r_con, **data)
        grant.save()
        grant = Grant.by_pk(r_con, grant.pk)
        assert grant.user.pk == user.pk
        assert grant.client_id == client.client_id
        assert grant.scopes == ['email', 'user']
        assert Grant.get_for_oauth2(r_con, client.client_id, '101112').pk == grant.pk

        class Request(object):
            scopes = ['email', 'user']

            def __init__(self, user):
                self.user = user

        request = Request(user=user)
        current_user = lambda: request.user
        grant = Grant.set_for_oauth2(r_con, current_user, 'abcdef', {'code': '123'}, request)

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
            'expires_in': 3600,
            'scope': ['email', 'user'],
        }

        token = Token(r_con, **token_data)
        token.save()

        token = Token.by_pk(r_con, token.pk)

        assert token.user.pk == user.pk
        assert token.client.pk == client.pk
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
            'scope': ['email', 'user'],
        }

        token = Token.set_for_oauth2(r_con, token_data, request)
        assert token.user.pk == user.pk
        assert token.client.pk == client.pk
        assert token.scopes == ['email', 'user']

        token = Token.get_for_oauth2(r_con, access_token='abc')
        assert token.user.pk == user.pk
        assert token.client.pk == client.pk
        assert token.scopes == ['email', 'user']

        token = Token.get_for_oauth2(r_con, refresh_token='123')
        assert token.user.pk == user.pk
        assert token.client.pk == client.pk
        assert token.scopes == ['email', 'user']


if __name__ == '__main__':
    unittest.main()
