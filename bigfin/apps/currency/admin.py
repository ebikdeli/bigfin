from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Currency


admin.site.register(Currency, SimpleHistoryAdmin)
