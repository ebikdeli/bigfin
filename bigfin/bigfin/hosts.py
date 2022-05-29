"""
We have used these docs to setup and lunch subdomains in the project:
https://django-hosts.readthedocs.io/en/latest/
https://simpleisbetterthancomplex.com/packages/2016/10/11/django-hosts.html

If we want to serve 'static' and 'media' resources that used in subdomains except for 'ROOT_URLCONF' we can use this:
    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
in any '<app>.urls.py' module! It's super eazy and barely an inconvinience!

Remember, redirecting urls with templatetags and reverse url are a little diffrent using subdomain and shown told in these docs!
"""

from django.conf import settings
from django_hosts import patterns, host


host_patterns = patterns('',
    # host('', settings.ROOT_URLCONF, name='www'),
    host(r'(|www)', settings.ROOT_URLCONF, name='www'),
    host(r'dashboard', 'apps.dashboard.urls', name='dashboard'),)
