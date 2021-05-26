from django.db import models
from bigfin.settings.dev import AUTH_USER_MODEL
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    phone = models.CharField(max_length=12)
    address = models.TextField(blank=True)
    credit = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # trades => list of all trades profile done
    # comments => list of all comments profile write
    # followers => List of all followers of profile
    # following => list of all people profile follows
    # likes => list of all profile likes
    # shares => list of all links profile shared

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_urls(self):
        return reverse('', kwargs={'id': self.id, 'slug': self.slug})
