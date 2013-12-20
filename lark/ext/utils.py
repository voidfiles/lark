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

        return super(DateTimeJSONEncoder, self).default(obj)

json_dumps = DateTimeJSONEncoder()
