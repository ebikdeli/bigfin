from django.db import models
from bigfin.settings.dev import AUTH_USER_MODEL
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='profile')
    phone = models.TextField(max_length=12)
    address = models.TextField(blank=True)
    credit = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # trades => list of all trades user done
    # comments => list of all comments user write
    # followers => List of all followers of user
    # following => list of all people user follows
    # likes => list of all user likes
    # shares => list of all links user shared

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_urls(self):
        return reverse('', kwargs={'id': self.id, 'slug': self.slug})