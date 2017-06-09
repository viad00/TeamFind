"""
Django settings for TeamFind project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2ce508b3-ae59-496b-8721-b456bc192698'
CRON_KEY = 'fctgiuhbvhgiucfsdriovdtfgyjjkgf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]
SOCIAL_AUTH_STEAM_API_KEY = 'F1A61ADB142308996B15FC20432579A6'
NOCAPTCHA = True
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']
AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/updateinfo'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/updateinfo'

# Application definition

INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'social_django',
    'bootstrapform',
    'captcha',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'TeamFind.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'TeamFind.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#App constants
#Ранги в игре
RANKS = (
        ('UN', 'Без ранга'),
        ('S1', 'Сильвер 1'),
        ('S2', 'Сильвер 2'),
        ('S3', 'Сильвер 3'),
        ('S4', 'Сильвер 4'),
        ('S5', 'Сильвер Элита'),
        ('S6', 'Сильвер Великий Магистр'),
        ('N1', 'Золотая Звезда 1'),
        ('N2', 'Золотая Звезда 2'),
        ('N3', 'Золотая Звезда 3'),
        ('N4', 'Золотая Звезда Магистр'),
        ('M1', 'Магистр Хранитель 1'),
        ('M2', 'Магистр Хранитель 2'),
        ('M3', 'Магистр Хранитель Элита'),
        ('M4', 'Заслуженный Магистр Хранитель'),
        ('L1', 'Легендарный Беркут'),
        ('L2', 'Легендарный Беркут Магистр'),
        ('SM', 'Великий Магистр Высшего Ранга'),
        ('GE', 'Всемирная Элита'),
    )
#Типы игр
TYPES = (
        ('MM', 'Соревновательный'),
        ('PU', 'Игры в лигах'),
        ('LE', 'Профессиональная Лига'),
        ('CA', 'Казуальный'),
    )
#Типы игроков
GAMERS = {
    'AWP':'Авапер',
    'LUK':'Люрк',
    'RIF':'Рифлер',
    'IGL':'Капитан',
    'SUP':'Саппорт',
    'FRG':'Фрагер',
    }
TYPES_SETTINGS = {'MM' : 0, 'PU' : 1, 'LE': 2, 'CA': 3}

ADMINS = [
    '76561198055294907',
]
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "teamfind"
    }
}
CACHE_TTL = 5