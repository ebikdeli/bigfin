from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    """Model for holding any currency"""
    name = models.CharField(verbose_name=_('crypto name'), max_length=100)
    symbol = models.CharField(verbose_name=_('symbol'), max_length=10)
    price = models.DecimalField(verbose_name=_('last price (usd)'), max_digits=17, decimal_places=10, default=0)
    time = models.DateTimeField(verbose_name=_('time'), auto_now=True, blank=True, null=True)
    founded = models.CharField(verbose_name=_('founded'), blank=True, null=True, max_length=4)
    is_crypto = models.BooleanField(verbose_name=_('is crypto'), default=False)

    class Meta:
        db_table = 'currency'

    def __str__(self):
        return f'{self.name}'.title()
