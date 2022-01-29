from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import uuid


class Wallet(models.Model):
    """Model for User wallet"""
    wallet_id = models.UUIDField(verbose_name=_('wallet id'), default=uuid.uuid4, editable=True)
    user = models.OneToOneField(to=get_user_model(),
                                related_name='wallet',
                                on_delete=models.CASCADE,
                                verbose_name=_('user'),)
    currencies = models.ManyToManyField('currency.Currency', related_name='wallets', verbose_name=_('currencies'))
    contents = models.JSONField(verbose_name=_('wallet contents'), blank=True, null=True)
    credit = models.DecimalField(verbose_name=_('user credit'), max_digits=9, decimal_places=0, default=0)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)

    def __str__(self):
        return f'{self.user.username}_wallet'
