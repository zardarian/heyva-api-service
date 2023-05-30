import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

# Create the Celery app
app = Celery("api")

# Load the Celery settings from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover and register tasks from all installed Django apps
app.autodiscover_tasks(["queue"])
