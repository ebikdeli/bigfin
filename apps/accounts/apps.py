from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'

    def ready(self):
        # x = self.get_model('User')
        # print('model   ', x.objects.all())
        from apps.accounts import signals
