Lark is RESTy inteface for redis
================================

.. image:: https://api.travis-ci.org/voidfiles/lark.png
    :target: https://travis-ci.org/voidfiles/lark


Lark provides a generic method from transforming a HTTP request into a redis command. If you have heard of `webdis <http://webd.is/>`_, the concept is familiar.

Features
________

* Support for RESTy interface ie. POST for writes, GET for reads, and DELETE for, well, deletes.
* Speaks JSON sending and recieving.
* Automatic JSON serilization and deserialization for redis values
* Automatic key prefixing for multi-user environments
* Fully tested adapaters for Flask, and Django
* Support for scopes based authorization with an eye towards hooking up with `flask-oauthlib <https://flask-oauthlib.readthedocs.org/en/latest/>`_
* While rough, documentation is available for `all supported methods <http://lark.readthedocs.org/en/latest/redis_api_client.html>`_


To get started make sure that you have redis installed, and then install lark.

::

    pip install lark


Next you can create a simple Flask app that mounts the lark blueprint.

::

	from flask import Flask
	from lark.ext.flask.redis_api import redis_api_blueprint
	from lark.ext.flask.flask_redis import Redis

	app = Flask(__name__)
	# Add a simpple redis connection to the global object
	Redis(app)

	app.config['DEFAULT_LARK_SCOPES'] = set(['admin'])

	# Mount the redis blueprint
	app.register_blueprint(redis_api_blueprint, url_prefix='/api/0')


	if __name__ == '__main__':
	    app.run()


From here you can run the server and then you will be able to interact with the API like so. You can find documentation on all the calls here.


::

	>>> curl http://127.0.0.1:5000/api/0/get/a/
	{"meta": {"status": "ok", "status_code": 200}


	>>> curl -X POST -H 'Content-Type: application/json' \
	--data-ascii '{"value": "foo"}' \
	http://127.0.0.1:5000/api/0/set/a/
	"meta": {"status": "ok", "status_code": 200}, "data": true}

	>>> curl http://127.0.0.1:5000/api/0/get/a/
	{"meta": {"status": "ok", "status_code": 200}, "data": "foo"}



Planned Features
________________

* Flask middleware to support oauth2
* A full Web interface for managing, and editing redis values.

