from datetime import datetime, timedelta
from flask import g, render_template, request, jsonify

from flask_oauthlib.provider import OAuth2Provider
import redis

from lark.auth.models import User, Client, Grant, Token
from lark.auth.oauth2 import bind_redis


def current_user():
    return g.user


r_con = redis.Redis.from_url('redis://localhost:6379/11')


def redis_provider(app):
    oauth = OAuth2Provider(app)

    bind_redis(oauth, r_con, user=User, token=Token,
               client=Client, grant=Grant, current_user=current_user)

    return oauth


def prepare_app(app):
    user = User(r_con, username='admin', password='admin')
    user.save()

    user2 = User(r_con, username='admin2', password='admin2')
    user2.save()

    client1 = Client(r_con, name='dev', client_id='dev', client_secret='dev',
                     default_scope=['address', 'email'],
                     user=user, redirect_uris=('http://localhost:8000/authorized',
                                               'http://localhost/authorized'))

    client1.save()

    client2 = Client(r_con, name='confidential', client_id='confidential',
                     default_scope=['address', 'email'],
                     client_secret='confidential', client_type='confidential',
                     user=user2, redirect_uris=('http://localhost:8000/authorized',
                                                'http://localhost/authorized'))

    client2.save()

    return app


def create_server(app, oauth):
    app = prepare_app(app)

    @app.before_request
    def load_current_user():
        user = User.by_pk(r_con, 1)
        g.user = user

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/oauth/authorize', methods=['GET', 'POST'])
    @oauth.authorize_handler
    def authorize(*args, **kwargs):
        # NOTICE: for real project, you need to require login
        if request.method == 'GET':
            # render a page for user to confirm the authorization
            return render_template('confirm.html')

        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'

    @app.route('/oauth/token')
    @oauth.token_handler
    def access_token():
        return {}

    @app.route('/api/email')
    @oauth.require_oauth('email')
    def email_api(oauth):
        return jsonify(email='me@oauth.net', username=oauth.user.username)

    @app.route('/api/client')
    @oauth.require_oauth()
    def client_api(oauth):
        return jsonify(client=oauth.client.name)

    @app.route('/api/address/<city>')
    @oauth.require_oauth('address')
    def address_api(oauth, city):
        return jsonify(address=city, username=oauth.user.username)

    @app.route('/api/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
    @oauth.require_oauth()
    def method_api(oauth):
        return jsonify(method=request.method)

    return app


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'development'
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.sqlite'
    })
    app = create_server(app)
    app.run()
