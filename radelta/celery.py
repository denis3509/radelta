import os

from celery.result import AsyncResult
from celery.signals import after_setup_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radelta.settings')
import django

django.setup()
from celery import Celery
import ast
import importlib

celery_app = Celery('app')
celery_app.config_from_object('radelta.celeryconfig')

celery_app.autodiscover_tasks()


@after_setup_logger.connect
def setup_loggers(*args, **kwargs):
    """use logging config in celery workers"""
    from logging.config import dictConfig
    dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "loguru": {
                "class": "core.logging.DjangoLoguruHandler",
            },
        },
        "root": {
            "handlers": ["loguru"],
            "level": "INFO",
        },
    })


class Queue:
    MAIN = "main"


def retry_celery_task(task_id: str):
    """retries celery task with given task id"""
    task_res = AsyncResult(task_id)
    task_meta = task_res._get_task_meta()
    if task_meta["status"] != 'FAILURE':
        raise Exception(f'{task_meta["task_id"]} => Skipped. Not in "FAILURE"')

    task_actual_name = task_meta["task_name"].split('.')[-1]
    module_name = '.'.join(task_meta["task_name"].split('.')[:-1])
    try:
        kwargs = ast.literal_eval(task_meta["task_kwargs"])
    except ValueError:
        kwargs = {}
    try:
        args = ast.literal_eval(task_meta["task_args"])
    except ValueError:
        args = []
    print(f"retrying {module_name}.{task_actual_name}")
    getattr(importlib.import_module(module_name), task_actual_name).apply_async(args=args,
                                                                                kwargs=kwargs,
                                                                                task_id=task_res.task_id)
    return f'{task_meta["task_id"]} => Successfully sent to queue for retry '
