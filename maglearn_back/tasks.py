import click
from celery import Celery
from flask.cli import with_appcontext

from maglearn_back.celeryconfig import CeleryConfig

celery = Celery(__name__, config_source=CeleryConfig)


def init_celery(celery_, app):
    """Initialize celery by introducing app context."""

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_.Task = ContextTask
    app.cli.add_command(celery_worker_command)


@click.command('celery-worker',
               context_settings={"ignore_unknown_options": True})
@click.argument('argv', nargs=-1)
@with_appcontext
def celery_worker_command(argv):
    """Command for running celery worker."""
    args = ['celery', 'worker', '-A', 'maglearn_back', '-P', 'gevent', *argv]
    click.echo(f"Starting Celery worker with arguments {args}.")
    celery.start(argv=args)
