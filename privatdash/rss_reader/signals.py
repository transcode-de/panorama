from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from privatdash.signals import side_navigation


@receiver(side_navigation, dispatch_uid="side_navigation_rss_reader")
def side_navigation_rss_reader(sender, **kwargs):
    return {
        'active_name': 'rss_reader',
        'css_classes': 'fa fa-rss',
        'title': _('RSS Reader'),
        'url': reverse('rss_reader_view'),
    }
