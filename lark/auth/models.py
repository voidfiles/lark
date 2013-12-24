from datetime import datetime, timedelta
import json

from flask.ext.bcrypt import Bcrypt
import iso8601
from lark.ext.utils import json_dumps


class StuctRedisModel(dict):
    key_prefix = None
    valid_attrs = tuple()
    indexes = tuple()

    def __setattr__(self, name, val):
        return self.__setitem__(name, val)

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __init__(self, r_con, **kwargs):
        self.r_con = r_con
        for attr in self.valid_attrs:
            self[attr] = kwargs.get(attr)

    @classmethod
    def from_data(cls, r_con, data):
        kwargs = json.loads(data)
        return cls(r_con, **kwargs)

    def to_dict(self):
        data = {}
        for attr in self.valid_attrs:
            data[attr] = self.get(attr)

        return data

    def items(self):
        return self.to_dict().items()

    def iteritems(self):
        return self.to_dict().iteritems()

    def serialize(self):
        data = self.to_dict()
        return json_dumps.encode(data)

    def for_json(self):
        return self.to_dict()

    def delete(self):
        if not self.pk:
            return self

        key_root = '%s' % (self.key_prefix)

        self.r_con.delete('%s:%s' % (key_root, self.pk))
        for index in self.indexes:
            self.r_con.delete('%s:%s:%s' % (key_root, index, self.get(index)))

        return self

    def save(self):
        if not self.pk:
            pk = self.r_con.incr('%s:_meta:pk' % self.key_prefix)
            self.pk = pk

        data = self.serialize()
        key_root = '%s' % (self.key_prefix)
        self.r_con.set('%s:%s' % (key_root, self.pk), data)
        for index in self.indexes:
            self.r_con.set('%s:%s:%s' % (key_root, index, getattr(self, index)), pk)

    def __repr__(self):
        return self.serialize()

    @classmethod
    def get_by_index(cls, r_con, index, *args):
        if index not in cls.indexes:
            raise Exception('%s not in indexes %s' % (index, cls.indexes))
        args = ':'.join(args)
        key = '%s:%s:%s' % (cls.key_prefix, index, args)
        pk = r_con.get(key)
        if pk:
            return cls.by_pk(r_con, pk)

        return None

    @classmethod
    def by_pk(cls, r_con, pk):
        key = '%s:%s' % (cls.key_prefix, pk)
        data = r_con.get(key)
        if data:
            return cls.from_data(r_con, data)

        return data

bcrypt = Bcrypt()


class User(StuctRedisModel):
    key_prefix = 'user'

    valid_attrs = (
        'pk',
        'username',
        'password_hash',
        'external_access_token',
        'remote_user_id',
        'extra_info'
    )

    indexes = (
        'username',
        'remote_user_id',
    )

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        if password:
            kwargs['password_hash'] = bcrypt.generate_password_hash(password)

        super(User, self).__init__(*args, **kwargs)

    @classmethod
    def get_for_oauth2(cls, r_con, username, password, client, request):
        user = cls.get_by_index(r_con, 'username', username)
        if not user:
            return None

        if not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user


class Client(StuctRedisModel):
    key_prefix = 'client'

    valid_attrs = (
        'pk',
        'name',
        'description',
        'user_pk',
        'client_id',
        'client_secret',
        'client_type',
        'default_scope',
        'redirect_uris',
        'extra_info'
    )

    indexes = (
        'client_id',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            kwargs['user_pk'] = user.pk

        if not kwargs.get('user_pk'):
            raise Exception('No user model assigned to client')

        super(Client, self).__init__(*args, **kwargs)

    @property
    def user(self):
        if not self.get('_user'):
            self['_user'] = User.by_pk(self.r_con, self.user_pk)

        return self['_user']

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        return self.default_scope

    @classmethod
    def get_for_oauth2(cls, r_con, client_id):
        client = cls.get_by_index(r_con, 'client_id', client_id)
        if not client:
            return None

        return client


class Grant(StuctRedisModel):
    key_prefix = 'grant'

    valid_attrs = (
        'pk',
        'user_pk',
        'client_id',
        'code',
        'redirect_uri',
        'scope',
        'expires',
        'allowed_grant_types',
        'allowed_response_types'
        'extra_info',
    )

    indexes = (
        'client_id_code',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            kwargs['user_pk'] = user.pk

        if not kwargs.get('user_pk'):
            raise Exception('No user model assigned to grant')

        expires_in = kwargs.pop('expires_in', None)
        if expires_in:
            expires = datetime.utcnow() + timedelta(seconds=expires_in)
        else:
            expires = 0

        kwargs['expires'] = kwargs.pop('expires', expires)
        super(Grant, self).__init__(*args, **kwargs)

    @property
    def expires(self):
        _expires = self.get('expires')
        if not _expires:
            return 0

        return iso8601.parse_date(_expires).replace(tzinfo=None)

    @property
    def client_id_code(self):
        return '%s:%s' % (self.client_id, self.code)

    @property
    def user(self):
        if not self.get('_user'):
            self['_user'] = User.by_pk(self.r_con, self.user_pk)

        return self['_user']

    @property
    def scopes(self):
        return self.scope

    @classmethod
    def get_for_oauth2(cls, r_con, client_id, code):

        if isinstance(code, dict):
            code = code.get('code')

        return cls.get_by_index(r_con, 'client_id_code', client_id, code)

    @classmethod
    def set_for_oauth2(cls, r_con, current_user, client_id, code, request):
        code = code.get('code')

        grant = {
            'client_id': client_id,
            'code': code,
            'user': current_user(),
            'scope': request.scopes,
            'expires_in': 600,
        }

        grant_inst = cls.get_for_oauth2(r_con, client_id, code)

        if grant_inst:
            return grant_inst

        grant = cls(r_con, **grant)
        grant.save()
        return grant


class Token(StuctRedisModel):
    key_prefix = 'token'

    valid_attrs = (
        'pk',
        'user_pk',
        'client_pk',
        'token_type',
        'access_token',
        'refresh_token',
        'expires',
        'scope',
        'extra_info',
    )

    indexes = (
        'access_token',
        'refresh_token',
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('token_type', 'bearer')
        user = kwargs.pop('user', None)
        if user:
            kwargs['user_pk'] = user.pk

        if not kwargs.get('user_pk'):
            raise Exception('No user model assigned to token')

        client = kwargs.pop('client', None)
        if client:
            kwargs['client_pk'] = client.pk

        expires_in = kwargs.pop('expires_in', None)
        if expires_in:
            expires = datetime.utcnow() + timedelta(seconds=expires_in)
        else:
            expires = 0

        kwargs['expires'] = kwargs.pop('expires', expires)
        scope = kwargs.pop('scope', [])
        if isinstance(scope, basestring):
            scope = scope.split(' ')

        kwargs['scope'] = scope
        super(Token, self).__init__(*args, **kwargs)

    @property
    def scopes(self):
        return self.scope

    @property
    def user(self):
        if not self.get('_user'):
            self['_user'] = User.by_pk(self.r_con, self.user_pk)

        return self['_user']

    @property
    def client(self):
        if not self.get('_client'):
            self['_client'] = Client.by_pk(self.r_con, self.client_pk)

        return self['_client']

    @property
    def client_id(self):
        return self.client.client_id

    @property
    def expires(self):
        _expires = self.get('expires')
        if not _expires:
            return 0

        return iso8601.parse_date(_expires).replace(tzinfo=None)

    @classmethod
    def get_for_oauth2(cls, r_con, access_token=None, refresh_token=None):
        token = None
        if access_token:
            token = cls.get_by_index(r_con, 'access_token', access_token)

        if not token and refresh_token:
            token = cls.get_by_index(r_con, 'refresh_token', refresh_token)

        if token:
            return token

        return token

    @classmethod
    def set_for_oauth2(cls, r_con, token, request, *args, **kwargs):
        token_data = {}
        token_data.update(token)
        token_data['client'] = request.client
        token_data['user'] = request.user
        token_already = cls.get_for_oauth2(r_con, token['access_token'])
        if token_already:
            return token_already

        token = cls(r_con, **token_data)
        token.save()

        return token
