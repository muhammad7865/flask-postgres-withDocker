from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flasgger import swag_from
import json

from paperclip.auth import bcrypt
from paperclip.db import db
from paperclip.models.user import User


user_api = Blueprint('api/user', __name__)


@user_api.route('/', methods=['POST'])
def create():
    payload = json.loads(request.data)
    email = payload['email'];

    if User.query.filter_by(email=email).first():
        return jsonify({ "error": "user already exists" }), 400

    password = bcrypt.generate_password_hash(payload['password']).decode('utf-8')

    user = User(name=payload['name'], email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(payload), 200

@user_api.route('/me', methods=['GET'])
@login_required
def read():
    return jsonify(current_user.to_json()), 200
