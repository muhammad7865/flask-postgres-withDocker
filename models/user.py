# from flask_login import login_manager

from paperclip.db import db
# from paperclip.auth import login_manager

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
        }

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
