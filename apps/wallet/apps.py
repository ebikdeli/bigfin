from django.apps import AppConfig


class WalletConfig(AppConfig):
    name = 'apps.wallet'

    def ready(self) -> None:
        from apps.wallet import signals
