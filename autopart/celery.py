from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autopart.settings')

app = Celery('autopart')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'delete-unpaid-orders-every-day': {
        'task': 'custom.tasks.delete_unpaid_orders',
        'schedule': crontab(hour=0, minute=5),  # Schedule task to run every day at midnight
    },
}