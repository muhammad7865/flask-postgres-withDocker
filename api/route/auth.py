from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
import json

# --- FIXED IMPORTS ---
from db import db
from auth import bcrypt
from models.user import User
# --- END OF FIXES ---


auth_api = Blueprint('api/auth', __name__)


@auth_api.route('/login', methods=['POST'])
def login():
    payload = json.loads(request.data)
    user = User.query.filter_by(email=payload['email']).first()
    if not user:
        return jsonify({"error": "user does not exist"}), 400

    if not bcrypt.check_password_hash(user.password, payload['password']):
        return jsonify({"error": "incorrect password"}), 400

    user.authenticated = True
    db.session.add(user)
    db.session.commit()
    login_user(user)

    return '', 200


@auth_api.route('/logout', methods=['POST'])
@login_required
def logout():
    current_user.authenticated = False
    db.session.add(current_user)
    db.session.commit()
    logout_user()
    return '', 200
