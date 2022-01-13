from django.db import models
import uuid

"""
class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    profile = models.ForeignKey(Profile,
                                related_name='wallets',
                                on_delete=models.CASCADE)
"""