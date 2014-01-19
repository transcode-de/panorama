from django.views.generic import TemplateView, ListView

from privatdash.views import ActiveNavMixin

from .models import RSSSource


class RSSReaderBaseView(ActiveNavMixin):
    sidenav_active = 'rss_reader'


class RSSReaderView(RSSReaderBaseView, TemplateView):
    template_name = 'rss_reader/rss_reader_view.html'


class RSSSourceListView(RSSReaderBaseView, ListView):
    model = RSSSource

    def get_queryset(self, *args, **kwargs):
        qs = super(RSSSourceListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)
