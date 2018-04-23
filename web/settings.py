"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z0lma)u2vzhs*5-3_2e^j)opymy1d4dv&15!lqlm0wza%%!ob^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.9.103', 'www.xuetangx.com',
                 'hunting-tracker', '127.0.0.1']

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'account',
    'common',
    'entry',
    'terminology',
    'script',
    'problem_classification',
    'cycle_task',
    'problem',
    'sso',
    'graph',
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

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "mysql.hunting_tracker.info",
        "NAME": "hunting_tracker",
        "PASSWORD": "",
        "PORT": "3306",
        "USER": "root",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    },
    'sso': {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "mysql.sso.info",
        "NAME": "permissions",
        "PASSWORD": "",
        "PORT": "3306",
        "USER": "root",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


REST_FRAMEWORK = {
    'SEARCH_PARAM': 'q',
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler'
}


# static server(storage)
STATIC_SERVER = {
    'FOLDER': 'hunting_tracker',
    'PUBLIC_API': 'http://gfsclient.xuetangx.info/upload',
    'PUBLIC_HOST': 'http://storage.xuetangx.info',
    'PATH_PREFIX': '/data/public',
}


# 执行脚本的服务器
EXECUTE_SERVER = [
    'localhost'
]


CELERY_BROKER_URL = 'amqp://huntingtracker:huntingtracker@localhost:5672//'

CELERY_BEAT_SCHEDULE = {
    'every-1-minute': {
        'task': 'cycle_task.tasks.ttt',
        # 'schedule': 10.0,
        'schedule': 63
    },
    'every-hour-begin': {
        'task': 'cycle_task.tasks.clean',
        'schedule': crontab(hour='*/1'),
    }
}
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_PREFETCH_MULTIPLIER = 1


