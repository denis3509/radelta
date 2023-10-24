from django.conf import settings
from rest_framework import views

from core.logging import get_logger

logger = get_logger()

def exception_handler(exc, context):
    response = views.exception_handler(exc, context)


    return response
