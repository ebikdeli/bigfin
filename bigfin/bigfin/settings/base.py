"""
Purpose of 'apps.py' in django applications:
https://docs.djangoproject.com/en/4.0/ref/applications/#configuring-applications
https://stackoverflow.com/questions/32795227/what-is-the-purpose-of-apps-py-in-django-1-9

We have used 'django-hosts' package to add subdomains to django site:
https://pypi.org/project/django-hosts/

** 'django-silk' is very very database intensive and could made our website so slow and our database full in just a short time.
Altought very useful analytical tool, we should only use it in development.
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
    'django_countries',
    'django_filters',
    # 'social_django',
    'channels',
    # These are some of 'jazzband' useful projects libraries. These tools are very helpful
    'taggit',
    'django_hosts',
    "debug_toolbar",
    'simple_history',
    'silk',
    'axes',

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
    
    # "debug_toolbar.middleware.DebugToolbarMiddleware",    This is wrong:
    # based on this doc, https://django-hosts.readthedocs.io/en/latest/faq.html
    # debug-toolbar must come after django-hosts request middleware and based on my experience it must just come before
    # django-hosts repsonse middleware to not get 'djdt' not fount error.

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'simple_history.middleware.HistoryRequestMiddleware',

    'silk.middleware.SilkyMiddleware',

    'axes.middleware.AxesMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'bigfin.urls'

# Django-hosts settings. Root hosts.py for subdomains
# https://jazzband.co/projects/django-hosts

ROOT_HOSTCONF = 'bigfin.hosts'

DEFAULT_HOST = 'www'

# Template settings

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

# Django-debug-toolbar
# https://jazzband.co/projects/django-debug-toolbar

INTERNAL_IPS = [
    "127.0.0.1",
    'localhost'
]

# django Silk optional settings:
# https://pypi.org/project/django-silk/

SILKY_PYTHON_PROFILER = True

SILKY_PYTHON_PROFILER_BINARY = True

SILKY_DYNAMIC_PROFILING = [{
    'module': 'apps.ticketing.views',
    'function': 'TicketingViewset.list'
}]

SILKY_ANALYZE_QUERIES = True

SILKY_MAX_RECORDED_REQUESTS = 10**3

SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10

# Change default settings for 'axes' to work well:
#https://django-axes.readthedocs.io/en/latest/2_installation.html

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]
