from braces.views import LoginRequiredMixin

from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from privatdash.views import ActiveNavMixin

from .forms import RSSSourceForm, RSSCategoryForm
from .models import RSSSource, RSSCategory, RSSEntry


class RSSReaderBaseView(LoginRequiredMixin, ActiveNavMixin):
    sidenav_active = 'rss_reader'


class RSSReaderDisplayBaseView(RSSReaderBaseView):

    def get_context_data(self, *args, **kwargs):
        context = super(RSSReaderDisplayBaseView, self).get_context_data(*args, **kwargs)
        context['view_active'] = True
        return context


class RSSReaderEditBaseView(RSSReaderBaseView):

    def get_context_data(self, *args, **kwargs):
        context = super(RSSReaderEditBaseView, self).get_context_data(*args, **kwargs)
        context['edit_active'] = True
        return context


class RSSSourceBaseView(RSSReaderEditBaseView):

    def get_context_data(self, *args, **kwargs):
        context = super(RSSSourceBaseView, self).get_context_data(*args, **kwargs)
        context['resource_active'] = True
        return context


class RSSCategoryBaseView(RSSReaderEditBaseView):

    def get_context_data(self, *args, **kwargs):
        context = super(RSSCategoryBaseView, self).get_context_data(*args, **kwargs)
        context['category_active'] = True
        return context


class RSSReaderView(RSSReaderDisplayBaseView, ListView):
    template_name = 'rss_reader/rss_reader_view.html'
    model = RSSEntry

    def get_context_data(self, *args, **kwargs):
        context = super(RSSReaderView, self).get_context_data(*args, **kwargs)
        context['categories'] = RSSCategory.objects.filter(user=self.request.user)
        return context


class RSSSourceListView(RSSSourceBaseView, ListView):
    model = RSSSource

    def get_queryset(self, *args, **kwargs):
        qs = super(RSSSourceListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user.pk)


class RSSSourceModelView(RSSSourceBaseView):
    model = RSSSource
    form_class = RSSSourceForm

    def get_success_url(self):
        return reverse('rss_reader_rsssource_list_view')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(RSSSourceModelView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs


class RSSSourceCreateView(RSSSourceModelView, CreateView):
    """ CreateView for RSSSource Objects. """


class RSSSourceUpdateView(RSSSourceModelView, UpdateView):
    """ UpdateView for RSSSource Objects. """


class RSSSourceDeleteView(RSSSourceModelView, DeleteView):
    """ DeleteView for RSSSource Objects. """


class RSSCategoryListView(RSSCategoryBaseView, ListView):
    model = RSSCategory

    def get_queryset(self, *args, **kwargs):
        qs = super(RSSCategoryListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user.pk)


class RSSCategoryModelView(RSSCategoryBaseView):
    model = RSSCategory
    form_class = RSSCategoryForm

    def get_success_url(self):
        return reverse('rss_reader_rsscategory_list_view')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(RSSCategoryModelView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs


class RSSCategoryCreateView(RSSCategoryModelView, CreateView):
    """ CreateView for RSSCategory Objects. """


class RSSCategoryUpdateView(RSSCategoryModelView, UpdateView):
    """ UpdateView for RSSCategory Objects. """


class RSSCategoryDeleteView(RSSCategoryModelView, DeleteView):
    """ DeleteView for RSSCategory Objects. """
