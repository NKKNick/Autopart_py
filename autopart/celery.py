from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autopart.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('autopart')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'delete-unpaid-orders-every-day': {
        'task': 'admin_app.tasks.delete_unpaid_orders',
        'schedule': 100.0,  # Schedule task to run every day at midnight
    },
    # Add other periodic tasks here
}
