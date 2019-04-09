import os

from flask import Flask

from .admin import admin
from .database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    sqlite_path = os.path.join(app.instance_path, 'maglearn-back.sqlite')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=sqlite_path,
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{sqlite_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        FLASK_ADMIN_SWATCH='flatly'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database.init_app(app)

    admin.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
