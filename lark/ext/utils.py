import datetime
import json


class RedisApiException(Exception):

    def __init__(self, message, status_code, *args, **kwargs):
        super(RedisApiException, self).__init__(message)
        self.status_code = status_code


class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, set):
            return list(obj)

        if obj and hasattr(obj, 'to_json'):
            obj = obj.to_json()
        print 'Trying to json encode %s' % (type(obj))
        return super(DateTimeJSONEncoder, self).default(obj)

json_dumps = DateTimeJSONEncoder()
