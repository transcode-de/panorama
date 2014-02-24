from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Widget(models.Model):
    user = models.ForeignKey(get_user_model())
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    widget_type = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Wiget Relation')
        verbose_name_plural = _('Widget Relations')
