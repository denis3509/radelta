import logging
from pathlib import Path

from django.conf import settings
from loguru import logger

logger.add(Path.joinpath(settings.LOG_DIR, "root.log"),
           format="{time} {level} {message} {exception}",
           level=settings.LOG_LEVEL.upper(),
           rotation="100 MB",
           serialize=True,
           diagnose=False,
           enqueue=True)

logger.add(Path.joinpath(settings.LOG_DIR, "celery.log"),
           format="{time} {level} {message} {exception}",
           level=settings.LOG_LEVEL.upper(),
           rotation="100 MB",
           serialize=True,
           filter=lambda record: record["extra"].get("logger_name", "").startswith("celery"),
           diagnose=False,
           enqueue=True)


def get_logger(name="root", *args, **kwargs):
    return logger.bind(logger_name=name)


def safe_record_message(message):
    return message.replace("<", "\<").replace(">", "\>")


class DjangoLoguruHandler(logging.Handler):
    """Handles records from python's logging and redirect it
    to loguru """

    def __init__(self, level=0, **kwargs):
        self.kwargs = kwargs
        print(kwargs)
        super(DjangoLoguruHandler, self).__init__(level)

    def emit(self, record) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelname

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.bind(logger_name=record.name).opt(
            exception=record.exc_info, depth=depth, lazy=True,
        ).log(level, safe_record_message(record.getMessage()))


