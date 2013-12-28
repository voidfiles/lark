import functools

from colander import Invalid
from redis.exceptions import DataError
from flask import Blueprint, make_response, g, request
from flask_oauthlib.provider import OAuth2Provider

from lark.ext.flask.flask_redis import Redis
from lark.ext.utils import json_dumps

from .models import User, Token, Client, Grant
from .schemas import ClientSchema
from .oauth2 import bind_models
from .database import db

oauth = OAuth2Provider()
redis = Redis()


class NotFound(Exception):
    pass


class NotAuthorized(Exception):
    pass


def current_user():
    return g.user


# Lazily register oauth, redis
def init_blueprint(state):
    oauth.init_app(state.app)
    redis.init_app(state.app)
    db.init_app(state.app)
    bind_models(oauth, user=User, token=Token,
                client=Client, grant=Grant, current_user=current_user)

lark_admin_api = Blueprint('lark_admin_api', __name__)
lark_admin_api.record(init_blueprint)


def api_func(func, oauth_obj, schema=None, *args, **kwargs):
    status_code = 200
    try:
        try:
            request_json = request.get_json()
        except:
            request_json = None

        if schema:
            schema_inst = schema()
            data = schema_inst.serialize(request_json)
        else:
            data = request_json

        if data:
            args = list(args) if args else []
            args.insert(0, data)

        data = func(oauth_obj, *args, **kwargs)

        resp_envelope = {
            'meta': {
                'status': 'ok',
                'status_code': status_code,
            },
            'data': data,
        }
    except NotFound, e:
        status_code = 404
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': status_code,
                'error_message': unicode(e)
            }
        }
    except NotAuthorized, e:
        status_code = 400
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': status_code,
                'error_message': unicode(e)
            }
        }
    except DataError, e:
        status_code = 400
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': status_code,
                'error_message': unicode(e)
            }
        }
    except Invalid, e:
        status_code = 400
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': status_code,
                'error_message': unicode(e)
            }
        }
    except Exception, e:
        raise
        status_code = 500
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': 500,
                'error_message': 'unhandled error'
            }
        }

    resp_json = json_dumps.encode(resp_envelope)
    return make_response(resp_json, status_code, {
        'Content-Type': 'application/json',
    })


def json_handler(schema=None):
    def outer_wraper(f):
        @functools.wraps(f)
        def wrapper(schema=None, *args, **kwargs):
            print f
            print schema
            return api_func(f, schema, *args, **kwargs)
        return wrapper
    return outer_wraper

# @app.route('/oauth/authorize', methods=['GET', 'POST'])
# @oauth.authorize_handler
# def authorize(*args, **kwargs):
#     # NOTICE: for real project, you need to require login
#     if request.method == 'GET':
#         # render a page for user to confirm the authorization
#         return render_template('confirm.html')

#     confirm = request.form.get('confirm', 'no')
#     return confirm == 'yes'


@lark_admin_api.route('/oauth/token')
@oauth.token_handler
def access_token():
    return {}


@lark_admin_api.route('/clients', methods=['POST'])
@oauth.require_oauth('admin')
@json_handler(schema=ClientSchema)
def create_client(oauth_obj, client):
    client = Client.create_from_user(oauth_obj.user, client)
    return client.for_api()


@lark_admin_api.route('/clients', methods=['GET'])
@oauth.require_oauth('admin')
@json_handler()
def get_clients(oauth_obj):
    clients = oauth_obj.user.clients
    clients = [client.for_api() for client in clients]
    return clients


def get_client_with_authorize(user, client_id):
    client = Client.query.filter_by(client_id=client_id).first()
    if not client:
        raise NotFound('Client for %s does not exsist' % client_id)

    if not client.authorized(user):
        raise NotAuthorized('You are not authorized to get this resource')

    return client


@lark_admin_api.route('/clients/<client_id>', methods=['GET'])
@oauth.require_oauth('admin')
@json_handler()
def get_client(oauth_obj, client_id):
    print oauth_obj.user
    client = get_client_with_authorize(oauth_obj.user, client_id)

    return client.for_api()


@lark_admin_api.route('/clients/<client_id>', methods=['POST'])
@oauth.require_oauth('admin')
@json_handler(schema=ClientSchema)
def update_client(oauth_obj, client_data, client_id):
    client = get_client_with_authorize(oauth_obj.user, client_id)
    client = client.update(client_data)

    return client.for_api()


@lark_admin_api.route('/clients/<client_id>/tokens', methods=['GET'])
@oauth.require_oauth('admin')
@json_handler()
def get_tokens(oauth_obj, client_id):
    client = get_client_with_authorize(oauth_obj.user, client_id)
    tokens = Token.get_by_index('user_pk', oauth_obj.user.pk)
    # Ensure user owns client
    # Find a list of this users tokens for this client


@lark_admin_api.route('/clients/<client_id>/tokens', methods=['POST'])
@oauth.require_oauth('admin')
@json_handler(schema=ClientSchema)
def create_token(oauth_obj, client_data, client_id):
    # Ensure user owns client
    class RequestValidator(object):
        def save_bearer_token(self, token, request):
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
