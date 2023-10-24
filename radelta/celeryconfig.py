from datetime import timedelta

from django.conf import settings

timezone = settings.CELERY_TIMEZONE
broker_url = settings.CELERY_BROKER_URL

result_backend = settings.CELERY_RESULT_BACKEND
cache_backend = settings.CELERY_CACHE_BACKEND
result_extended = settings.CELERY_RESULT_EXTENDED
result_expires = timedelta(days=7)
# worker_hijack_root_logger = False
