import os
from flask import Flask, render_template
from flasgger import Swagger

# --- Use DIRECT imports for local modules ---
from auth import login_manager, bcrypt
from config import get_db_uri
from db import db, migrate
from models.user import User
from api.route.home import home_api
from api.route.auth import auth_api
from api.route.user import user_api
# --- End DIRECT imports ---


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SECRET_KEY'] = 'a_very_secret_key'  # Replace 'secret' with a better default
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    app.config['SWAGGER'] = {
        'title': 'Flask API Boilerplate - Docs',
        'uiversion': 3,
        'specs_route': '/apidocs/'  # Make sure swagger UI route is explicit
    }

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Initialize swagger (do not assign to an unused variable)
    Swagger(app)

    # Register blueprints
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(auth_api, url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/user')

    return app


@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
        return User.query.get(user_id)
    except (TypeError, ValueError):
        return None


@login_manager.request_loader
def request_loader(request):
    # NOTE: request parsing for 'email' should be implemented where request data is available
    # Keep the existing behavior: if 'email' is provided, try to load the user
    email = None
    try:
        # attempt to get email from form or args; this is a best-effort placeholder
        email = request.form.get('email') if request.form else None
    except Exception:
        email = None

    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            return user  # Return user if found based on email in form
    return None


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/users')
def users_page():
    return render_template('users.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


if __name__ == '__main__':
    # Do not enable debug mode or bind to all interfaces by default.
    # Control via environment in development or Docker as needed.
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    app.run(host=host, port=port, debug=debug)
