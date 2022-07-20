from pathlib import Path
import os
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-vicn8!qw(2fu+a-5h=moz0dhrzkf-(q!*2=6eq-k2p2g@xqh0='
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'atent.apps.AuthenticationConfig',
    'form',
]
MIDDLEWARE_CLASSES = ['dev.middleware.LoginRequiredMiddleware',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR , 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dev.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.myhost.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'myemail.com'
EMAIL_HOST_PASSWORD = 'mypasword'
EMAIL_USE_TLS = True

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

from django.utils.translation import gettext_lazy as _
LANGUAGES= [
    ('fa', _('Persian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join(BASE_DIR , 'assets'),)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
