from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.signals import side_navigation, widget_types, extra_js, extra_css

from .models import RSSWidget
from .forms import RSSWidgetForm


@receiver(side_navigation, dispatch_uid="side_navigation_rss_reader")
def side_navigation_rss_reader(sender, **kwargs):
    return {
        'active_name': 'rss_reader',
        'css_classes': 'fa fa-rss',
        'title': _('RSS Reader'),
        'url': reverse('rss_reader_view'),
    }


@receiver(widget_types, dispatch_uid="widget_types_rss_reader")
def widget_types_rss_reader(sender, **kwargs):
    ct = ContentType.objects.get_for_model(RSSWidget)
    return {
        'pk': ct.pk,
        'name': 'RSS Widget',
        'form': RSSWidgetForm
    }


@receiver(extra_js, dispatch_uid="extra_js_rss_widgets")
def extra_js_rss_widgets(sender, **kwargs):
    return ['js/rss_reader.js']


@receiver(extra_css, dispatch_uid="extra_css_rss_widgets")
def extra_css_rss_widgets(sender, **kwargs):
    return ['css/rss_widget.css']
