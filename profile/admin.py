from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from profile.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['phone', 'address',
              'credit', 'score', ]


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

