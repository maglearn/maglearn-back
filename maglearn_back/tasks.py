from celery import Celery


# Needs to be accessible from top level to be used as decorator
celery = Celery(__name__, broker="redis://localhost:6379") # TODO: broker is fixed and not configurable for now


def init_app(app):
    """Initialize app by creating Celery instance"""
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
