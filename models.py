from enum import Enum

from flask_login import AnonymousUserMixin, UserMixin

from app import db

GUEST_USER = -1
NORMAL_USER = 0
ADMIN_USER = 1


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    progress = db.Column(db.Integer, nullable=True)
    role = db.Column(db.Integer, nullable=False)

    def get_id(self):
        return self.id


class AnonymousUser(AnonymousUserMixin):
    role = GUEST_USER


class Slide(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=False)
    image = db.Column(db.String(60), nullable=False, default='default.png')
    time = db.Column(db.String(8), nullable=False)

    def tojson(self):
        """Returns a JSON serializable dicionary representing the class."""
        return { 'title': self.title, 'image': self.image, 'time': self.time }
