from datetime import datetime

from maglearn_back.database import db


class User(db.Model):
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', name='user_fk'))
    author = db.relationship('User', foreign_keys=[author_id])
    created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)


class Dataset(db.Model):
    input_size = db.Column(db.Integer, nullable=False)
    output_size = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    source_function = db.Column(db.String, nullable=False)
    data = db.Column(db.JSON, nullable=False)


class NetworkArchitectureDefinition(db.Model):
    type = db.Column(db.String, nullable=False)
    definition = db.Column(db.JSON, nullable=False)