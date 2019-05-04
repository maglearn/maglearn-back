import os

from flask import Flask
from flask_graphql import GraphQLView

from maglearn_back import model, tasks, admin, database, auth, blog, datasets


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    sqlite_path = os.path.join(app.instance_path, 'maglearn-back.sqlite')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=sqlite_path,
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{sqlite_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        FLASK_ADMIN_SWATCH='flatly',
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    for module in [admin, database, model, tasks]:
        module.init_app(app)

    for module in [auth, blog, datasets]:
        app.register_blueprint(module.bp)
    app.add_url_rule('/', endpoint='index')

    from . import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema.schema,
            graphiql=True
        )
    )

    return app
