# django_celery/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techcruncherapp.settings")

app = Celery("techcruncherapp")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Set the maximum interval for Celery Beat
app.conf.beat_max_loop_interval = 1800  # 30 minutes in seconds

app.autodiscover_tasks()