"""
This module uses 'content type' to upload files. We can use documentations here:
https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/

Remember that if we want flexibility for the Generic model, we better to set 'content_type' and 'content_object'
fields to null for the model. Like the things we did on FileUpload model.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

import datetime
import uuid


def file_upload_to(instance, filename):
    """Function that saves user ticket file to a good path"""
    today = str(datetime.date.today())
    if isinstance(instance, get_user_model().__class__):
        return f'user/{today}/{instance.username}/{filename}'
    if isinstance(instance, Ticketing().__class__):
        return f'ticketing/{today}/{instance.user.username}_sent/{filename}'
    if isinstance(instance, Answer().__class__):
        return f'ticketing/{today}/{instance.ticketing.user.username}_answered/{filename}'
    return f'{today}/{filename}'


class FileUpload(models.Model):
    """FileUpload model is content type model that holds every file we want to upload for every model in the project"""
    file = models.FileField(verbose_name=_('attach file (if any)'), upload_to=file_upload_to, blank=True, null=True)
    caption = models.CharField(verbose_name=_('caption'), max_length=200, blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    history = HistoricalRecords()

    def __str__(self):
        return f'File({self.id})'


class Ticketing(models.Model):
    """This model represents Tickets that user creates"""
    EMERGENCY_CHOISES = [
        ('1', _('Not Important')),
        ('2', _('Little Important')),
        ('3', _('Important')),
        ('4', _('Very Important')),
        ('5', _('Very High Important'))
    ]

    ticket_id = models.UUIDField(verbose_name=_('ticket id'), default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(),
                             related_name='user_tickets',
                             on_delete=models.CASCADE,
                             verbose_name=_('user'))
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='group_tickets',
                              verbose_name=_('group'),
                              blank=True,
                              null=True)
    title = models.CharField(verbose_name=_('title'), max_length=100)
    emergency = models.CharField(verbose_name=_('emergency'), max_length=1, choices=EMERGENCY_CHOISES, default='3')
    message = models.TextField(verbose_name=_('message'))
    is_published = models.BooleanField(verbose_name=_('is published'), default=True)
    is_answered = models.BooleanField(verbose_name=_('is answered'), default=False)
    files = GenericRelation('FileUpload', related_query_name='ticketing')
    # file = models.FileField(verbose_name=_('attach file (if any)'), upload_to=file_upload_to, blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    history = HistoricalRecords()


class Answer(models.Model):
    """For every Ticketing model, there would be unlimited Answers"""
    ticketing = models.ForeignKey('Ticketing',
                                  on_delete=models.CASCADE,
                                  related_name='ticketing_answers',
                                  verbose_name=_('ticketing'))
    user = models.ForeignKey(get_user_model(),
                             related_name='user_answers',
                             on_delete=models.CASCADE,
                             verbose_name=_('user'))
    message = models.TextField(verbose_name=_('message'))
    # file = models.FileField(verbose_name=_('attach file (if any)'), upload_to=file_upload_to, blank=True, null=True)
    files = GenericRelation(FileUpload, related_query_name='answer')
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id}_{self.message[:10]}'
