from django.conf import settings
from django.http import HttpResponse
import json
from redis.exceptions import DataError

from colander import Invalid
from lark.redis.client import RedisApiClient
from lark.ext.utils import json_dumps, RedisApiException


redis_connection = getattr(settings, 'REDIS_CONNECTION_METHOD', None)
if not redis_connection:
    raise Exception("Lark requires a way to connect to redis please set REDIS_CONNECTION_METHOD in your settings.py")

r = redis_connection()


class InvalidMethod(Exception):
    pass


def query_redis(request, *args, **kwargs):
    status_code = 200
    try:
        methods = kwargs.pop('methods', ['GET'])
        redis_method = kwargs.pop('redispy_method')
        if request.method not in methods:
            raise InvalidMethod()

        request_json = None
        if request.method == 'POST':
            try:
                request_json = json.loads(request.body.decode(encoding='UTF-8'))
            except:
                pass

        scopes = None
        default_scopes = getattr(settings, 'DEFAULT_LARK_SCOPES', set())

        scope_getter = getattr(settings, 'LARK_SCOPE_GETTER', None)
        if scope_getter:
            scopes = scope_getter(request, redis_method, request_json, request.GET, args, kwargs)

        if scopes is None:
            scopes = default_scopes

        data = RedisApiClient.from_request(redis_method, r, request_json, request.GET, args, kwargs, scopes)
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
    except RedisApiException, e:
        status_code = e.status_code
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': e.status_code,
                'error_message': unicode(e)
            }
        }

    except InvalidMethod, e:
        status_code = 405
        resp_envelope = {
            'meta': {
                'status': 'error',
                'status_code': 405,
                'error_message': '%s Invalid method should be one of %s' % (request.method, methods)
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
    return HttpResponse(resp_json, content_type='application/json', status=status_code)
