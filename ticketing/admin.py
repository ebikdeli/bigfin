from django.contrib import admin

from ticketing.models import Ticketing, Answer

admin.site.register([Ticketing, Answer])
