from braces.views import LoginRequiredMixin, JSONResponseMixin, CsrfExemptMixin
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.template import loader, Context
from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import SingleObjectMixin
from core.views import ActiveNavMixin

from .forms import RSSSourceForm, RSSCategoryForm, RSSWidgetForm
from .models import RSSSource, RSSCategory, RSSEntry, RSSWidget



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
    category = None
    source = None

    def get_context_data(self, *args, **kwargs):
        context = super(RSSReaderView, self).get_context_data(*args, **kwargs)
        context['categories'] = RSSCategory.objects.filter(user=self.request.user)
        context['sources'] = RSSSource.objects.filter(user=self.request.user)
        if self.category:
            context['category_active'] = True
            context['heading'] = '%(category)s: %(category_title)s' % {
                'category': _(u'Category'), 'category_title': self.category.title
            }
        elif self.source:
            context['source_active'] = True
            context['heading'] = '%(source)s: %(source_title)s' % {
                'source': _(u'Source'), 'source_title': self.source.title
            }
        else:
            context['all_active'] = True
            context['heading'] = _(u'all Entries')
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(RSSReaderView, self).get_queryset(*args, **kwargs).filter(
            rss_source__user=self.request.user)
        if 'category' in self.request.GET:
            self.category = RSSCategory.objects.get(pk=self.request.GET.get('category'))
            qs = qs.filter(rss_source__categories=self.category.pk)
        elif 'source' in self.request.GET:
            self.source = RSSSource.objects.get(pk=self.request.GET.get('source'))
            qs = qs.filter(rss_source=self.source.pk)
        return qs


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


class RSSEntryMarkReadView(RSSReaderBaseView, SingleObjectMixin, View):
    """ Mark entry as read. """
    model = RSSEntry

    def get_object(self):
        qs = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is not None:
            qs = qs.filter(pk=pk)
        else:
            raise AttributeError("RSSEntryMarkReadView must be called with "
                             "either an object pk or a slug.")
        qs = qs.filter(rss_source__user=self.request.user)
        try:
            obj = qs.get()
        except self.model.ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': qs.model._meta.verbose_name})
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_new = False
        self.object.save()
        return HttpResponse()


class RSSWidgetBaseView(LoginRequiredMixin, ActiveNavMixin):
    form_class = RSSWidgetForm
    model = RSSWidget
    sidenav_active = 'dashboard'
    template_name = 'panorama/widget_form.html'

    def get_success_url(self):
        return reverse('dashboard')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(RSSWidgetBaseView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs


class RSSWidgetCreateView(CsrfExemptMixin, RSSWidgetBaseView, JSONResponseMixin, CreateView):
    """ Create View for RSSWidget objects. """

    def render_to_response(self, context, **response_kwargs):
        t = loader.get_template(self.template_name)
        c = Context(context)
        json = {'html': t.render(c)}
        return self.render_json_response(json)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        super(RSSWidgetCreateView, self).form_valid(form)
        return self.render_json_response({
            'location': reverse('dashboard'),
            'html': '<h2>Success! The page will be immediately reloaded...</h2>'
        })
