import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigfin.settings.dev')

app = Celery(main='bigfin', broker='amqp://ehsan:Ehsan1992@localhost:5672/ehsanhost', backend='amqp://ehsan:Ehsan1992@localhost:5672/ehsanhost')
# app = Celery('bigfin', broker='redis://localhost:6379', backend='redis://localhost:6379')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
