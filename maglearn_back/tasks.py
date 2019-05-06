import click
from celery import Celery
from celery.bin import worker
from celery.utils.log import LOG_LEVELS
from flask.cli import with_appcontext

from maglearn_back.celeryconfig import CeleryConfig

celery = Celery(__name__, config_source=CeleryConfig)

# TODO: consider alternative to Celery i.e. Dramatiq


def init_celery(celery_, app):
    """Initialize celery by introducing app context."""

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_.Task = ContextTask
    app.cli.add_command(celery_worker_command)


@click.command('celery-worker')
@click.option('--loglevel', default='INFO', show_default=True,
              type=click.Choice([l for l in LOG_LEVELS if isinstance(l, str)]),
              help='Celery worker log level.')
@with_appcontext
def celery_worker_command(loglevel):
    """Command for running celery worker."""
    click.echo("Starting Celery worker.")
    options = {
        'loglevel': loglevel,
        'traceback': True,
        'pool': 'gevent'
    }
    worker.worker(app=celery).run(**options)
