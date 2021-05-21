from .base import *

DEBUG = True

SECRET_KEY = '+4@22_0@5f@@)sj$v@gj@q$jghm!q!c$m%v*bgu)1fcy*=t4a*'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass

