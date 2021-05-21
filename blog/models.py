from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class BlogPage(Page):
    body = RichTextField()
    images = models.ImageField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='body'),
        FieldPanel('images', classname='image')
    ]
