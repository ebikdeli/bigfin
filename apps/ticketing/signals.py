from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import uuid


@receiver(post_save, sender='ticketing.Ticketing')
def ticket_uuid(sender, instance, **kwargs):
    """Check if there is uuid on ticketing"""
    if not instance.ticket_id:
        instance.ticket_id = str(uuid.uuid4())
        instance.save()


@receiver(post_save, sender='ticketing.Answer')
def is_answered_ticketing(sender, instance, created, **kwargs):
    """If is_staff create answer, Ticketing is_answered flag turn to True"""
    if created:
        if instance.user.is_staff:
            instance.ticketing.is_answered = True
            instance.ticketing.save()
        else:
            instance.ticketing.is_answered = False
            instance.ticketing.save()
