from django.views.generic import TemplateView

from privatdash.views import ActiveNavMixin


class RSSReaderView(ActiveNavMixin, TemplateView):
    sidenav_active = 'rss_reader'
    template_name = 'rss_reader/rss_reader_view.html'
