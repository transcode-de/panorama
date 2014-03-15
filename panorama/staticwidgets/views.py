from braces.views import LoginRequiredMixin, JSONResponseMixin, CsrfExemptMixin
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.views.generic import CreateView

from .forms import WeatherWidgetForm
from .models import WeatherWidget


class WeatherWidgetCreateView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, CreateView):
    """ Create View for WeatherWidget objects. """
    template_name = 'panorama/widget_form.html'
    form_class = WeatherWidgetForm
    model = WeatherWidget

    def get_success_url(self):
        return reverse('dashboard')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(WeatherWidgetCreateView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def render_to_response(self, context, **response_kwargs):
        t = loader.get_template(self.template_name)
        c = Context(context)
        json = {'html': t.render(c)}
        return self.render_json_response(json)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        super(WeatherWidgetCreateView, self).form_valid(form)
        return self.render_json_response({
            'location': reverse('dashboard'),
            'html': '<h2>Success! The page will be immediately reloaded...</h2>'
        })
