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


class ExperimentDefinition(db.Model):
    backend = db.Column(db.String, nullable=False)
    reduction_algorithm = db.Column(db.String, nullable=False)
    metaparameters = db.Column(db.JSON)

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    dataset = db.relationship('Dataset')
    arch_definition_id = db.Column(db.Integer,
                                   db.ForeignKey(NetworkArchitectureDefinition.id))
    arch_definition = db.relationship('NetworkArchitectureDefinition')


class ExperimentJob(db.Model):
    start_date = db.Column(db.TIMESTAMP)
    end_date = db.Column(db.TIMESTAMP)

    definition_id = db.Column(db.Integer,
                              db.ForeignKey(ExperimentDefinition.id))
    definition = db.relationship('ExperimentDefinition')
    result = db.relationship('ExperimentResult', uselist=False,
                             back_populates='job')


class ExperimentResult(db.Model):
    execution_time = db.Column(db.Integer, nullable=False)
    training_history = db.Column(db.JSON, nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey(ExperimentJob.id),
                       unique=True)
    job = db.relationship('ExperimentJob', back_populates='result')

