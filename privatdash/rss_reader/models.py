import feedparser
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _

from time import mktime


class RSSCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=300)
    user = models.ForeignKey(get_user_model())

    def __unicode__(self):
        return self.title


class RSSSource(models.Model):
    title = models.CharField(verbose_name=_('Title'), blank=True, max_length=300,
        help_text=_('If no title is specified, the title of the rss feed will be used.'))
    description = models.TextField(verbose_name=_('Description'), max_length=1000, blank=True)
    categories = models.ManyToManyField(RSSCategory, blank=True)
    source = models.URLField(verbose_name=_('Source Url'),
        help_text=_('Source URL of the RSS Feed'))
    user = models.ForeignKey(get_user_model())
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('RSS Source')
        verbose_name_plural = _('RSS Sources')

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.source

    def entries_count(self):
        return self.entries.count()

    def unread_entries_count(self):
        return self.entries.filter(is_new=True).count()

    def save(self, *args, **kwargs):
        super(RSSSource, self).save(*args, **kwargs)
        self.update_feed_entries()

    def update_feed_entries(self):
        feed = feedparser.parse(self.source)
        if feed.bozo == 0:
            for entry in feed.entries:
                if not self.entries.filter(guid=entry.id).count():
                    self.entries.create(title=entry.title, description=entry.summary,
                        link=entry.link, is_new=True, guid=entry.id,
                        publishing_date=datetime.fromtimestamp(mktime(entry.published_parsed)))


class RSSEntry(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=300)
    description = models.TextField(verbose_name=_('Description'))
    link = models.URLField(verbose_name=_('Link to Entry'))
    is_new = models.BooleanField(verbose_name=_('Is new?'), default=True)
    rss_source = models.ForeignKey(RSSSource, related_name='entries')
    publishing_date = models.DateTimeField(verbose_name=_('Publishing Date'))
    guid = models.CharField(verbose_name=_('Unique Feed ID'), max_length=1000)


    class Meta:
        verbose_name = _('RSS Entry')
        verbose_name_plural = _('RSS Entry')
        ordering = ['-publishing_date', 'title']
        unique_together = ('guid', 'rss_source')

    def __unicode__(self):
        return self.title


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

    sources = models.ManyToManyField(RSSSource, related_name='sources')
    categories = models.ManyToManyField(RSSCategory)
    widget_type = models.SmallIntegerField(verbose_name=_('RSS Display Type'), choices=RSS_WIDGET_TYPE)

    class Meta:
        verbose_name = _('RSS Widget')
        verbose_name_plural = _('RSS Widgets')
