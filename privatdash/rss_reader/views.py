from braces.views import LoginRequiredMixin

from django.views.generic import TemplateView, ListView, CreateView

from privatdash.views import ActiveNavMixin

from .forms import RSSSourceCreateForm
from .models import RSSSource


class RSSReaderBaseView(LoginRequiredMixin, ActiveNavMixin):
    sidenav_active = 'rss_reader'


class RSSReaderView(RSSReaderBaseView, TemplateView):
    template_name = 'rss_reader/rss_reader_view.html'


class RSSSourceListView(RSSReaderBaseView, ListView):
    model = RSSSource

    def get_queryset(self, *args, **kwargs):
        qs = super(RSSSourceListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user.pk)


class RSSSourceAddView(RSSReaderBaseView, CreateView):
    model = RSSSource
    form_class = RSSSourceCreateForm
    success_url = 'rss_reader_rsssource_list_view'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(RSSSourceAddView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs
