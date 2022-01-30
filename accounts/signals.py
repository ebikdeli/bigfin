from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from rest_framework.authtoken.models import Token

import decimal


@receiver(pre_save, sender=get_user_model())
def validate_user_discount_percent(sender, instance, **kwargs):
    """Count user account discount"""
    if instance.discount_percent > 100:
        raise ValidationError(_('discount percent could not be more than 100'))

    elif instance.discount_percent < 0:
        raise ValidationError(_('discount percent could not be less than 0'))


@receiver(pre_save, sender=get_user_model())
def count_user_score_and_profile_discount(sender, instance, **kwargs):
    """Count user account score"""
    def score_count_helper(instance_score, discount_multiplier):
        """Helper function for DRY"""
        instance.discount_value += decimal.Decimal(10000 * discount_multiplier)
        instance.score_lifetime += instance_score
        instance.score = 0
    score = instance.score
    if 500 <= score <= 1000:
        score_count_helper(score, 1)
    elif 1000 < score <= 1500:
        score_count_helper(score, 2)
    elif instance.score > 1500:
        score_count_helper(score, 3)


@receiver(pre_save, sender=get_user_model())
def fill_slug_field(sender, instance, **kwargs):
    """Fill slug field for user"""
    if not instance.slug:
        instance.slug = slugify(instance.username)


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create Authentication token for newly created user"""
    if created:
        Token.objects.create(user=instance)
