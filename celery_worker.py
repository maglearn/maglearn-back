from maglearn_back.tasks import celery, init_celery
from maglearn_back import create_app

app = create_app()
init_celery(celery, app)
