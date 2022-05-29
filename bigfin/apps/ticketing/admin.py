"""
To use Genreic relations in admin panel use these documents:
1- https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#generic-relations-in-admin
2- https://docs.djangoproject.com/en/dev/ref/contrib/admin/#using-generic-relations-as-an-inline
"""
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from simple_history.admin import SimpleHistoryAdmin

from apps.ticketing.models import Ticketing, Answer, FileUpload

# This is used if 'FileUpload' was not exist: #
# admin.site.register([Ticketing, Answer])

class FileUploadInline(GenericTabularInline):
    """This is used to use generic relation field as regular inline model relations"""
    model = FileUpload


class TicketingAdmin(admin.ModelAdmin):
    inlines = [
        FileUploadInline,
    ]


class AnswerAdmin(admin.ModelAdmin):
    inlines = [
        FileUploadInline,
    ]


# Customized History for admin
class TicketHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['name', 'user__username']

admin.site.register(Ticketing, TicketingAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(FileUpload, SimpleHistoryAdmin)
