from flask import Flask
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

    # --- Configuration ---
    # Load DB URI from config function (which reads .env)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    # Explicitly set SECRET_KEY (can also be moved to .env via config.py if preferred)
    app.config['SECRET_KEY'] = 'a_very_secret_key' # Replace 'secret' with a better default
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking

    # Swagger Config
    app.config['SWAGGER'] = {
        'title': 'Flask API Boilerplate - Docs',
        'uiversion': 3,
        "specs_route": "/apidocs/" # Make sure swagger UI route is explicit
    }
    swagger = Swagger(app) # Initialize Swagger AFTER config

    # --- Blueprints ---
    # Register blueprints (routes)
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(auth_api, url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/user')

    # --- Extensions ---
    # Initialize extensions AFTER config and blueprints
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app

# --- Flask-Login Callbacks ---
@login_manager.user_loader
def load_user(user_id):
    # user_id is expected to be unicode, convert to int if necessary
    try:
        user_id = int(user_id)
        return User.query.get(user_id)
    except (TypeError, ValueError):
        return None


@login_manager.request_loader
def request_loader(request):
    # Simple token-based or session check could go here if needed later
    # For now, just rely on user_loader and session
    email = request.form.get('email') # Check if email is in form for basic login attempt
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            return user # Return user if found based on email in form
    return None # Otherwise, no user loaded from request directly


# Create the app instance for Gunicorn to find
app = create_app()


# --- CLI Runner (for local development only, not used by Gunicorn) ---
if __name__ == '__main__':
    # Note: Gunicorn runs 'app:app', so this block isn't executed by Docker CMD
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True is okay for Docker if needed temporarily

