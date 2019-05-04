from celery import Celery

# TODO: broker is fixed and not configurable for now
celery = Celery(__name__, broker="redis://localhost:6379")


def init_celery(celery, app):
    """Initialize celery by introducing app context."""
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
