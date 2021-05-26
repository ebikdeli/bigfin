from django.db import models
from django.template.defaultfilters import slugify

from django_countries.fields import CountryField


class FiatCurrency(models.Model):
    name = models.CharField(max_length=30)
    country = CountryField()
    founded = models.CharField(max_length=4, blank=True)
    value = models.PositiveIntegerField(verbose_name='Value compared to USD:')
    description = models.TextField(blank=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['value', 'founded']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DigitalCurrency(models.Model):
    TOKEN_OR_COIN = (
        ('Token', 'token'),
        ('Coin', 'coin')
    )
    name = models.CharField(max_length=30)
    founded = models.CharField(max_length=4, blank=True)
    value = models.PositiveIntegerField(verbose_name='Value compared to USD:')
    description = models.TextField(blank=True)
    slug = models.SlugField()
    token_or_coin = models.CharField(max_length=5, choices=TOKEN_OR_COIN)
    created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['value', 'founded']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
