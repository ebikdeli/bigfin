from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='profile')
    phone = models.TextField(max_length=12)
    address = models.TextField(blank=True)
    credit = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
