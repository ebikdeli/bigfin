from django.apps import AppConfig


class TicketingConfig(AppConfig):
    name = 'ticketing'

    def ready(self):
        from . import signals
