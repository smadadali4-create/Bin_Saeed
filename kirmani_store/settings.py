import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-pt+&xe8l40%rp7c1(475c14jp7ak=pf54r2iusb%m*isdgedpa')

DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost,.onrender.com', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'products',
    'cart',
    'orders',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kirmani_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_total',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'kirmani_store.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

import dj_database_url
db_url = config('DATABASE_URL', default='')
if db_url:
    DATABASES['default'] = dj_database_url.parse(db_url, conn_max_age=600)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

SITE_NAME = 'BIN SAEED OUTLET'
CONTACT_PHONE = '03097950381'
CONTACT_WHATSAPP = '03097950381'
CONTACT_EMAIL = 'contact@kirmanistore.com'

PAYMENT_METHODS = {
    'jazzcash': {
        'number': '03220654138',
        'name': 'BIN SAEED OUTLET',
        'instructions': 'Send payment to JazzCash number 03220654138. Use your Order ID as reference.'
    },
    'easypaisa': {
        'number': '03356232071',
        'name': 'BIN SAEED OUTLET',
        'instructions': 'Send payment to EasyPaisa account 03356232071. Use your Order ID as reference.'
    },
    'raast': {
        'number': '03136232071',
        'name': 'BIN SAEED OUTLET',
        'instructions': 'Send payment via Raast to 03136232071. Use your Order ID as reference.'
    },
    'cash': {
        'instructions': 'Pay cash when you receive your order at your doorstep.'
    },
}
