from flask_login import UserMixin
from db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    authenticated = db.Column(db.Boolean(), unique=False, nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    def __repr__(self):
        return f'<User {self.name}>'
