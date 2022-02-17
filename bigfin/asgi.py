"""
ASGI config for bigfin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/

*** Because 'Windows' could not support latest version of redis, redis_channels has problems channels.
To solve this problem we use 'channels'==3.0.3 and 'channels_redis'==2.4.0 or earlier version. Some document
says we can use https://www.memurai.com/ a replacement for redis in 'Windows' OS.
For more information about resolving channels and redis errors read below documents:
https://stackoverflow.com/questions/62786988/redis-err-unknown-command-bzpopmin
https://channels.readthedocs.io/en/latest/releases/3.0.0.html
https://stackoverflow.com/questions/64668204/attributeerror-type-object-chatconsumer-has-no-attribute-as-asgi
We are using django-channels in this project. More information about install and setup channels read below document:
https://channels.readthedocs.io/en/stable/installation.html
"""
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigfin.settings.dev')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
