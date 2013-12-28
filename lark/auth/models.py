from datetime import datetime, timedelta
import json

from flask.ext.bcrypt import Bcrypt
from lark.ext.utils import generate_random_string
from sqlalchemy.types import TypeDecorator, TEXT

from .database import db


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(40), nullable=False)
    external_access_token = db.Column(db.String(255), nullable=True)
    remote_user_id = db.Column(db.Integer)
    extra_info = db.Column(JSONEncodedDict)

    @classmethod
    def create_user(cls, **kwargs):
        password = kwargs.pop('password', None)
        if password:
            kwargs['password_hash'] = bcrypt.generate_password_hash(password)

        user = cls(**kwargs)
        db.session.add(user)
        db.session.commit()

        return user

    def for_api(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def check_password(self, password):
        hashed_password = bcrypt.generate_password_hash(password)
        return hashed_password == self.password

    @classmethod
    def get_for_oauth2(cls, username, password, client, request):
        user = cls.query.filter_by(username=username).first()
        if not user:
            return None

        if not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user


class Client(db.Model):
    # human readable name, not required
    name = db.Column(db.String(40))

    # human readable description, not required
    description = db.Column(db.String(400))

    # creator of the client, not required
    user_id = db.Column(db.ForeignKey('user.id'))
    # required if you need to support client credential
    user = db.relationship('User', backref="clients")

    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean, default=True)

    _redirect_uris = db.Column(db.Text, default='http://localhost:8000')
    _alowed_grant_types = db.Column(db.Text)
    _alowed_response_types = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)
    extra_info = db.Column(JSONEncodedDict)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def alowed_grant_types(self):
        if self._alowed_grant_types:
            return self._alowed_grant_types.split()
        return []

    @property
    def alowed_response_types(self):
        if self._alowed_response_types:
            return self._alowed_response_types.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

    def update(self, data):
        self.name = data.get('name')
        self.description = data.get('description')
        self._redirect_uris = ' '.join(data.get('redirect_uris'))

        db.session.add(self)
        db.session.commit()
        return self

    def for_api(self):
        return {
            'name': self.name,
            'description': self.description,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uris': self.redirect_uris,
            'user': self.user.for_api()
        }

    def authorized(self, user):
        return self.user.id == user.id

    @classmethod
    def get_for_oauth2(cls, client_id):
        return cls.query.filter_by(client_id=client_id).first()

    @classmethod
    def create_from_user(cls, user, data):
        while True:
            client_id = generate_random_string(32)
            client = cls.query.filter_by(client_id=client_id).first()
            if not client:
                break

        data['client_id'] = client_id
        data['client_secret'] = generate_random_string(32)
        data['user_id'] = user.id
        data['is_confidential'] = True
        data['_default_scopes'] = ''
        data['_redirect_uris'] = ' '.join(data.pop('redirect_uris', []))
        client = cls(**data)
        db.session.add(client)
        db.session.commit()

        return client


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)
    extra_info = db.Column(JSONEncodedDict)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    @classmethod
    def get_for_oauth2(cls, client_id, code):

        if isinstance(code, dict):
            code = code.get('code')

        return cls.query.filter_by(client_id=client_id, code=code).first()

    @classmethod
    def set_for_oauth2(cls, current_user, client_id, code, request):
        # decide the expires time yourself
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=current_user(),
            expires=expires
        )
        db.session.add(grant)
        db.session.commit()
        return grant


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)
    extra_info = db.Column(JSONEncodedDict)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    @classmethod
    def get_for_oauth2(cls, access_token=None, refresh_token=None):
        if access_token:
            return cls.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return cls.query.filter_by(refresh_token=refresh_token).first()

    @classmethod
    def set_for_oauth2(cls, token, request, *args, **kwargs):
        toks = Token.query.filter_by(client_id=request.client.client_id,
                                     user_id=request.user.id)

        # make sure that every client has only one token connected to a user
        for t in toks:
            db.session.delete(t)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)
        scopes = token['scope']
        if scopes and not isinstance(scopes, basestring):
            scopes = ' '.join(scopes)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=scopes,
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )
        db.session.add(tok)
        db.session.commit()
        return tok
