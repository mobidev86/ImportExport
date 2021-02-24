from __future__ import absolute_import
from celery import Celery
import os

from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Import_Export.settings')
app = Celery('Import_Export', include=["product.tasks"])

app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {

    # 'send_email_every-15-seconds': {
    #     'task': 'product.tasks.handle_file_task',
    #     'schedule': 15,
    #     'args': ('1',),
    # },
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
