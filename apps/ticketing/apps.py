from django.apps import AppConfig


class TicketingConfig(AppConfig):
    name = 'apps.ticketing'

    def ready(self):
        from . import signals
