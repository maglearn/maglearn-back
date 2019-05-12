from datetime import datetime

import click
import math
import petname
from flask.cli import with_appcontext

from maglearn_back.database import db, init_db
from maglearn_back.library.backend import Backend
from maglearn_back.library.data_generation import generate_random_fun_samples, \
    DampedSineWave
from maglearn_back.library.networks import NetworkType


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
    name = db.Column(db.String, nullable=False,
                     default=lambda: petname.generate(3))
    input_size = db.Column(db.Integer, nullable=False)
    output_size = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    source_function = db.Column(db.String, nullable=False)
    data = db.deferred(db.Column(db.JSON, nullable=False))


class NetworkArchitectureDefinition(db.Model):
    type = db.Column(db.Enum(NetworkType), nullable=False)
    definition = db.Column(db.JSON, nullable=False)


class ExperimentDefinition(db.Model):
    backend = db.Column(db.Enum(Backend), nullable=False)
    reduction_algorithm = db.Column(db.String, nullable=False)
    meta_parameters = db.Column(db.JSON)

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


def populate_db():
    """Populate database with dummy data."""
    dataset1_size = 150
    x, y = generate_random_fun_samples(DampedSineWave(), dataset1_size,
                                       (-4 * math.pi, 4 * math.pi),
                                       noise=True)
    dataset1_data = {'x': x.tolist(), 'y': y.tolist()}
    dataset1 = Dataset(input_size=1, output_size=1, size=dataset1_size,
                       source_function='exp(-lambda*x") * cos(omega *x * phi)',
                       data=dataset1_data)
    db.session.add(dataset1)

    arch_defn1 = NetworkArchitectureDefinition(type=NetworkType.MLP,
                                               definition={'input': 1,
                                                           'output': 1,
                                                           'hidden': [10, 10]})
    db.session.add(arch_defn1)

    experiment1 = ExperimentDefinition(backend=Backend.PYTORCH,
                                       reduction_algorithm='NONE',
                                       dataset=dataset1,
                                       arch_definition=arch_defn1)
    db.session.add(experiment1)

    db.session.commit()


@click.command('populate-db')
@click.option('--force', '-f', is_flag=True,
              help="Drop and recreate database forcefully first.")
@with_appcontext
def populate_db_command(force=False):
    """Populate data with dummy data."""
    if force:
        init_db()
    populate_db()
    click.echo('Populated the database.')


def init_app(app):
    app.cli.add_command(populate_db_command)
