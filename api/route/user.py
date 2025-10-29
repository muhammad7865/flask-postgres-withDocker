from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
import json

# --- FIXED IMPORTS ---
from auth import bcrypt
from db import db
from models.user import User
# --- END OF FIXES ---


user_api = Blueprint('api/user', __name__)


@user_api.route('/', methods=['POST'])
def create():
    payload = json.loads(request.data)
    email = payload['email']

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "user already exists"}), 400

    password = bcrypt.generate_password_hash(payload['password']).decode('utf-8')

    user = User(name=payload['name'], email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(payload), 200


@user_api.route('/me', methods=['GET'])
@login_required
def read():
    return jsonify(current_user.to_json()), 200
