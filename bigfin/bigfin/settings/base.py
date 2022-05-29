"""
Purpose of 'apps.py' in django applications:
https://docs.djangoproject.com/en/4.0/ref/applications/#configuring-applications
https://stackoverflow.com/questions/32795227/what-is-the-purpose-of-apps-py-in-django-1-9

We have used 'django-hosts' package to add subdomains to django site:
https://pypi.org/project/django-hosts/
"""
# from pathlib import Path
import os
from django.urls import reverse_lazy


# BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django_extensions',

    'rest_framework',
    'rest_framework.authtoken',
    'taggit',
    'django_countries',
    'django_filters',
    # 'social_django',
    'channels',
    'django_hosts',

    # 'todo',
    
    'apps.vitrin',
    'apps.api',
    'apps.chat',
    'apps.currency',
    'apps.blog',
    'apps.tutorial',
    'apps.accounts',
    'apps.dashboard',
    'apps.wallet',

    'apps.ticketing',
]

SITE_ID = 1

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'bigfin.urls'

# Root hosts.py for subdomains
ROOT_HOSTCONF = 'bigfin.hosts'

DEFAULT_HOST = 'www'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR)],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]
# We are using django-channels and we are using 'ASGI' so it must be above 'WSGI_APPLICATION' attribute.
ASGI_APPLICATION = 'bigfin.asgi.application'

# Channel layer configs:
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

WSGI_APPLICATION = 'bigfin.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

# Authentication settings

AUTH_USER_MODEL = 'accounts.User'
"""
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '501246578971-mjnug89a0d06euip8so4th7c5dikac2d.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'yChaL7cwc_nAUdYYJP42GwB5'
"""
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATICFILES_DIRS = [os.path.join(BASE_DIR)]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

LOGIN_URL = 'home'
LOGIN_REDIRECT_URL = reverse_lazy('vitrin:index')
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = reverse_lazy('vitrin:index')

# Rest framework settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}
