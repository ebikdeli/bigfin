"""
We are using subdomains to better manage our project. With subdomains, no longer 'urls.py' module used first. Instead
'hosts.py' module used first.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path("__reload__/", include("django_browser_reload.urls")),     # 'django-browser-reload' module
    # path('silk/', include('silk.urls', namespace='silk')),
    # path('grappelli/', include('grappelli.urls')),
    path('watchman/', include('watchman.urls')),    # Enable 'django-watchman'

    path('accounts/', include('apps.accounts.urls')),
    # path('dashboard/', include('apps.dashboard.urls')),   # It's a subdomain
    path('api/', include('apps.api.urls')),
    path('ticket/', include('apps.ticketing.urls')),
    path('chat/', include('apps.chat.urls')),
    path('', include('apps.vitrin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
