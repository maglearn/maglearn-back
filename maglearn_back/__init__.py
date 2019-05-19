import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_graphql import GraphQLView

from maglearn_back import model, admin, database, auth, blog, datasets, schema
from maglearn_back.api import restplus
from maglearn_back.tasks import celery, init_celery


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # TODO: 12.05.2019 John - configure cors
    CORS(app)
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

    # Extensions
    for module in [admin, database, model, restplus]:
        module.init_app(app)

    # Blueprints
    for module in [auth, blog, datasets]:
        app.register_blueprint(module.bp)
    app.add_url_rule('/', endpoint='index')

    # Celery
    init_celery(celery, app)

    # GraphQL
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema.schema,
            graphiql=True
        )
    )

    # Bootstrap
    Bootstrap(app)

    return app
