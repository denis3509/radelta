"""
Django settings for radelta project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path


def env(key, type_, default=None):
    """"reads env variable"""
    if key not in os.environ:
        if default is not None:
            return default
        else:
            raise ValueError(f"Expected environment variable with key {key}")
    val = os.environ[key]

    if type_ == str:
        return str(val)
    elif type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    elif type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%3@)km@e2)(1#xnm58oi_60&uxi6f$r6=b*c05(7a0&qj)14u0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django_celery_results',
    'drf_spectacular',
    'delivery',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'radelta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'radelta.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     'NAME': env("MYSQL_DATABASE", str),
    #     'USER': env("MYSQL_USER", str),
    #     'PASSWORD': env("MYSQL_PASSWORD", str),
    #     'HOST': env("MYSQL_HOST", str),
    #     'PORT': env("MYSQL_PORT", str),
    #
    #     "OPTIONS": {
    #         # 'NAME': env("MYSQL_DATABASE", str),
    #         # 'USER': env("MYSQL_USER", str),
    #         # 'PASSWORD': env("MYSQL_PASSWORD", str),
    #         # 'HOST': env("MYSQL_HOST", str),
    #         # 'PORT': env("MYSQL_PORT", str),
    #
    #     },
    # }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sessions

# Project
LOG_DIR = env('LOG_DIR', str, Path.joinpath(BASE_DIR, 'logs'))
LOG_LEVEL = env('LOG_LEVEL', str, 'debug')

# Cache
REDIS_PORT = env("REDIS_PORT", int)
REDIS_HOST = env("REDIS_HOST", str)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{REDIS_URL}/1",
    }
}

# DRF

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'core.drf.exception_handler'
}
# Spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'RA Delta',
    'DESCRIPTION': 'Test task',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "loguru": {
            "class": "core.logging.DjangoLoguruHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["loguru"],
            "level": "INFO",
        },
        "celery": {
            "handlers": ["loguru"],
            "level": "INFO",
        },
        "celery.beat": {
            "handlers": ["loguru"],
            "level": "INFO",
        },
    },
    # "root": {
    #     "handlers": ["loguru"],
    #     "level": "INFO",
    # },
}

# CELERY
CELERY_TIMEZONE = "UTC"
CELERY_BROKER_URL = f"{REDIS_URL}/0"

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_RESULT_EXTENDED = True
# for mysql
# DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH=191
