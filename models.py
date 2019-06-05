from enum import Enum

from flask_login import AnonymousUserMixin, UserMixin

from app import db

collaborators_table = db.Table(
    'collaborators',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
)

GUEST_USER = -1
NORMAL_USER = 0
CREATOR_USER = 1
ADMIN_USER = 2


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    progress = db.relationship('Progress', backref='user')
    role = db.Column(db.Integer, nullable=False)

    def get_id(self):
        return self.id


class AnonymousUser(AnonymousUserMixin):
    role = GUEST_USER


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    index = db.Column(db.Integer, nullable=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    slides = db.relationship('Slide', backref='course', lazy=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collaborators = db.relationship('User', secondary=collaborators_table, backref=db.backref('courses'))
    viewers = db.relationship('Progress', backref='course')


class Slide(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=False)
    image = db.Column(db.String(60), nullable=False, default='default.png')
    time = db.Column(db.String(8), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def tojson(self):
        """Returns a JSON serializable dicionary representing the class."""
        return {'title': self.title, 'image': self.image, 'time': self.time}
