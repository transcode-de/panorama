from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _


class RSSCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=300)
    user = models.ForeignKey(get_user_model())


class RSSSource(models.Model):
    title = models.CharField(verbose_name=_('Title'), blank=True, max_length=300)
    description = models.TextField(verbose_name=_('Description'), max_length=1000, blank=True)
    categories = models.ManyToManyField(RSSCategory)
    source = models.URLField(verbose_name=_('Source Url'))
    user = models.ForeignKey(get_user_model())

    class Meta:
        verbose_name = _('RSS Source')
        verbose_name_plural = _('RSS Sources')


class RSSEntry(models.Model):
    title = models.CharField(verbose_name=_('Title'), blank=True, max_length=300)
    description = models.TextField(verbose_name=_('Description'), max_length=1000)
    text = models.TextField(verbose_name=_('Text'), max_length=1000)
    link = models.URLField(verbose_name=_('Link to Entry'))
    is_new = models.BooleanField(verbose_name=_('Is new?'), default=True)
    rss_source = models.ForeignKey(RSSSource)
    publishing_date = models.DateField(verbose_name=_('Publishing Date'))

    class Meta:
        verbose_name = _('RSS Entry')
        verbose_name_plural = _('RSS Entry')
        ordering = ['-publishing_date', 'title']


class RSSWidget(models.Model):
    ALL_SOURCES_RSS_WIDGET = 0
    SINGLE_SOURCE_RSS_WIDGET = 1
    MULTI_SOURCE_RSS_WIDGET = 2
    CATEGORY_RSS_WIDGET = 3
    RSS_WIDGET_TYPE = (
        (ALL_SOURCES_RSS_WIDGET, _('All Sources Widget')),
        (MULTI_SOURCE_RSS_WIDGET, _('Selected Sources Widget')),
        (CATEGORY_RSS_WIDGET, _('Category Widget')),
    )

    class Meta:
        verbose_name = _('RSS Widget')
        verbose_name_plural = _('RSS Widgets')

    sources = models.ManyToManyField(RSSSource, related_name='sources')
    categories = models.ManyToManyField(RSSCategory)
    widget_type = models.SmallIntegerField(verbose_name=_('RSS Display Type'), choices=RSS_WIDGET_TYPE)
