from flask import Flask
from flasgger import Swagger

from paperclip.auth import login_manager, bcrypt
from paperclip.config import get_db_uri, get_secret_key
from paperclip.db import db, migrate
from paperclip.models.user import User
from paperclip.api.route.home import home_api
from paperclip.api.route.auth import auth_api
from paperclip.api.route.user import user_api


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SECRET_KEY'] = 'secret'
    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    swagger = Swagger(app)

    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(auth_api, url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/user')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    return User.query.filter_by(email=email).first()

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()

    app.run(host='0.0.0.0', port=5000, debug=True)
