from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.wallet.models import Wallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_after_user_created(sender, instance, created=None, **kwargs):
    """Create a wallet when a user created"""
    # https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/
    if created or not hasattr(instance, 'wallet_user'):
        Wallet.objects.create(user=instance)
