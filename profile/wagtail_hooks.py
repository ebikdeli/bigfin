from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from profile.models import Profile


class ProfileAdmin(ModelAdmin):
    model = Profile
    menu_label = 'Profile'
    menu_order = 200
    list_display = ['user', 'phone', 'address',
                    'picture', 'credit', 'score', ]
    search_fields = ['user', 'phone', 'credit', 'score', ]
    list_filter = ['address']


modeladmin_register(ProfileAdmin)
