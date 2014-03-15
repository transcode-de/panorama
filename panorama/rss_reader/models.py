import feedparser

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from time import mktime

import pytz
utc=pytz.UTC

from core.signals import side_navigation, widget_types, extra_js, extra_css


class RSSCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=300)
    user = models.ForeignKey(get_user_model())

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('categories')
        ordering = ['title']

    def __unicode__(self):
        return self.title


class RSSSource(models.Model):
    title = models.CharField(verbose_name=_('Title'), blank=True, max_length=300,
        help_text=_('If no title is specified, the title of the rss feed will be used.'))
    categories = models.ManyToManyField(RSSCategory, blank=True)
    source = models.URLField(verbose_name=_('Source Url'),
        help_text=_('Source URL of the RSS Feed'))
    user = models.ForeignKey(get_user_model())
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('RSS Source')
        verbose_name_plural = _('RSS Sources')
        ordering = ['updated', 'title']

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
        self.updated = timezone.now()
        super(RSSSource, self).save(*args, **kwargs)
        self.update_feed_entries()

    def update_feed_entries(self):
        feed = feedparser.parse(self.source)
        if feed.bozo == 0:
            for entry in feed.entries:
                if not self.entries.filter(guid=entry.id).count():
                    published_unaware = timezone.datetime.fromtimestamp(
                        mktime(entry.updated_parsed))
                    published = utc.localize(published_unaware)
                    kwargs = dict(title=entry.title, description=entry.summary,
                        link=entry.link, is_new=True, guid=entry.id,
                        publishing_date=published)
                    if 'author' in entry.keys():
                        kwargs['author'] = entry.get('author')
                    self.entries.create(**kwargs)


class RSSEntry(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=300)
    description = models.TextField(verbose_name=_('Description'))
    link = models.URLField(verbose_name=_('Link to Entry'))
    is_new = models.BooleanField(verbose_name=_('Is new?'), default=True)
    rss_source = models.ForeignKey(RSSSource, related_name='entries')
    publishing_date = models.DateTimeField(verbose_name=_('Publishing Date'))
    guid = models.CharField(verbose_name=_('Unique Feed ID'), max_length=1000)
    author = models.CharField(verbose_name=_('Author'), max_length=300, blank=True)


    class Meta:
        verbose_name = _('RSS Entry')
        verbose_name_plural = _('RSS Entry')
        ordering = ['-publishing_date', 'title']
        unique_together = ('guid', 'rss_source')

    def __unicode__(self):
        return self.title


class RSSWidget(models.Model):
    TEMPLATE_NAME = 'rss_reader/widget.html'
    ICON_CLASS = 'fa fa-rss'
    WIDGET_CLASS = 'rss-widget'
    IS_REFRESHABLE = True

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    sources = models.ManyToManyField(RSSSource, related_name='sources', blank=True)
    categories = models.ManyToManyField(RSSCategory, blank=True)
    only_new = models.BooleanField(verbose_name=_('Show only new entries'))
    num_of_entries = models.IntegerField(verbose_name=_('How many entries should be shown?'),
        default=3)

    class Meta:
        verbose_name = _('RSS Widget')
        verbose_name_plural = _('RSS Widgets')

    def render(self, user, widget_pk):
        entries = RSSEntry.objects.filter(rss_source__user=user)
        categories = self.categories.all()
        sources = self.sources.all()
        if categories:
            entries = entries.filter(rss_source__categories__in=categories)
        if sources:
            entries = entries.filter(rss_source__in=sources)
        if self.only_new:
            entries = entries.filter(is_new=self.only_new)
        t = loader.get_template(self.TEMPLATE_NAME)
        c = Context({
            'object': self,
            'entries': entries[:self.num_of_entries],
            'widget_pk': widget_pk,
        })
        return t.render(c)


@receiver(side_navigation, dispatch_uid="side_navigation_rss_reader")
def side_navigation_rss_reader(sender, **kwargs):
    return {
        'active_name': 'rss_reader',
        'icon_classes': 'fa fa-rss',
        'title': _('RSS Reader'),
        'url': reverse('rss_reader_view'),
    }


@receiver(widget_types, dispatch_uid="widget_types_rss_reader")
def widget_types_rss_reader(sender, **kwargs):
    ct = ContentType.objects.get_for_model(RSSWidget)
    return {
        'pk': ct.pk,
        'name': 'RSS Widget',
        'form': 'rss_reader.forms.RSSWidgetForm'
    }


@receiver(extra_js, dispatch_uid="extra_js_rss_widgets")
def extra_js_rss_widgets(sender, **kwargs):
    return ['js/rss_reader.js']


@receiver(extra_css, dispatch_uid="extra_css_rss_widgets")
def extra_css_rss_widgets(sender, **kwargs):
    return ['css/rss_widget.css']
