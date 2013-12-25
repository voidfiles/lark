import functools

from colander import Invalid
from redis.exceptions import DataError
from flask import Blueprint, make_response, g, request
from flask_oauthlib.provider import OAuth2Provider

from lark.ext.flask.flask_redis import Redis
from lark.ext.utils import json_dumps

from .models import User, Token, Client, Grant
from .schemas import ClientSchema
from .oauth2 import bind_redis

oauth = OAuth2Provider()
redis = Redis()


def current_user():
    return g.user


# Lazily register oauth, redis
def init_blueprint(state):
    oauth.init_app(state.app)
    redis.init_app(state.app)
    bind_redis(oauth, redis.connect('admin'), user=User, token=Token,
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

        data = func(oauth_obj, data, *args, **kwargs)
        resp_envelope = {
            'meta': {
                'status': 'ok',
                'status_code': status_code,
            },
            'data': data,
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
    client = Client.create_from_user(g.get_redis_connection('admin'), oauth_obj.user, client)
    return client.for_api()
