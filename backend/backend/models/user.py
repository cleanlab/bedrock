from backend.models import db

import hashlib
import os


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(64), nullable=True)
    status = db.Column(db.Text, nullable=True)

    def __init__(self, username, password):
        self.username = username
        # this is not a good password hash, but we're doing it this way to keep
        # it simple
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.token = None

    @classmethod
    def by_username(cls, username):
        return cls.query.filter(cls.username == username).one_or_none()

    @classmethod
    def login(cls, username, password):
        user = cls.by_username(username)
        if user is None:
            return None
        if hashlib.sha256(password.encode()).hexdigest() != user.password_hash:
            return None
        # generate new token, return it
        user.token = os.urandom(32).hex()
        return user.token

    @classmethod
    def check_token(cls, username, token):
        user = cls.by_username(username)
        if user is None:
            return False
        if user.token is None or token != user.token:
            return False
        return True

    @classmethod
    def by_token(cls, token):
        return cls.query.filter(cls.token == token).one_or_none()
