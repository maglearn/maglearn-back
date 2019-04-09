import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, Integer, TIMESTAMP


class Base(Model):
    # this id implementation does not support inheritance
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_ts = Column(TIMESTAMP, default=datetime.now)
    update_ts = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<{type(self).__name__} #{self.id} >'


db = SQLAlchemy(model_class=Base)


def get_db():
    """Creates if needed, stores in g object and returns db connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Closes database connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize database schema."""
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    db.init_app(app)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

