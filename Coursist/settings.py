"""
Django settings for Coursist project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from logging import NOTSET, WARNING, CRITICAL
from sys import stdout, stderr

import requests

from academic_helper.utils.environment import is_prod
from academic_helper.utils.sentry import init_sentry

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "coursist.xyz"]

if is_prod():
    try:
        internal_ip = requests.get("http://instance-data/latest/meta-data/local-ipv4").text
    except requests.exceptions.ConnectionError:
        pass
    else:
        ALLOWED_HOSTS.append(internal_ip)
    del requests

DEBUG = not is_prod()

SECRET_KEY = os.getenv("SECRET_KEY", "6*cne7$@#zo,;gl7#$%^*HSfda,msp2-034u5jt'vf=jvhj")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    # Rating
    "reviews",
    "star_ratings",
    # Cron
    "django_cron",
    # Db backup
    "dbbackup",
    # Our app
    "academic_helper",
    # Health check
    "health_check",
    # "schedule",
    # Django base
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Facebook login
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    # "allauth.socialaccount.providers.google",
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Coursist.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Coursist.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3"), }}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

LOGGING_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGGING_DIR, exist_ok=True)

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {"format": "[%(asctime)s] [%(module)s/%(lineno)s] [%(threadName)s] - [%(levelname)s]: %(message)s"},
        "simple": {"format": "[%(asctime)s] [%(levelname)-.4s]: %(message)s", "datefmt": "%Y-%m-%d %H:%M:%S"},
    },
    "filters": {
        # "require_debug_true": {"()": "django.utils.log.RequireDebugTrue",},
        "std_filter": {"()": "academic_helper.utils.logger.LevelFilter", "low": NOTSET, "high": WARNING},
        "err_filter": {"()": "academic_helper.utils.logger.LevelFilter", "low": WARNING, "high": CRITICAL},
    },
    "handlers": {
        "console_out": {
            "class": "logging.StreamHandler",
            "filters": ["std_filter"],
            "formatter": "simple",
            "stream": stdout,
        },
        "console_err": {
            "class": "logging.StreamHandler",
            "filters": ["err_filter"],
            "formatter": "simple",
            "stream": stderr,
        },
        "debug_handler": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGGING_DIR, "django.log"),
            "formatter": "verbose",
        },
        "requests_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "requests.log"),
            "when": "D",
            "formatter": "verbose",
        },
        "site_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOGGING_DIR, "coursist.log"),
            "when": "D",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "coursist": {"handlers": ["console_out", "console_err", "site_handler"], "level": "DEBUG", "propagate": True},
        "django": {"handlers": ["console_out", "debug_handler"], "level": "INFO", "propagate": True, },
        "django.request": {"handlers": ["requests_handler"], "level": "INFO", "propagate": True},
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

AUTH_USER_MODEL = "academic_helper.CoursistUser"

LANGUAGE_CODE = "en-US"

TIME_ZONE = "Asia/Jerusalem"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

# Auth
AUTH_ACTIVATION = False
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "none"

# DB Backup
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "./backups"}

# Star rating
STAR_RATINGS_STAR_HEIGHT = 16
# STAR_RATINGS_ANONYMOUS = False
# STAR_RATINGS_RATING_MODEL = "academic_helper.ExtendedRating"

# Reviews
REVIEW_PUBLISH_UNMODERATED = True
REVIEW_SHOW_RATING_TEXT = False

# Cron
CRON_CLASSES = [
    "academic_helper.logic.crons.BackupCron",
]
