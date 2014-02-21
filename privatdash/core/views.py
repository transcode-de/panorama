from braces.views import LoginRequiredMixin, JSONResponseMixin

from django.template import loader, Context
from django.views.generic import ListView, FormView

from .signals import widget_types, extra_js
from .models import Widget


class ActiveNavMixin(object):
    sidenav_active = 'dashboard'

    def get_context_data(self, *args, **kwargs):
        context = super(ActiveNavMixin, self).get_context_data(*args, **kwargs)
        context['sidenav_active'] = self.sidenav_active
        return context


class Dashboard(LoginRequiredMixin, ActiveNavMixin, ListView):
    template_name = 'privatdash/dashboard.html'
    model = Widget

    def get_query_set(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(*args, **kwargs)
        context['widget_types'] = [widget_type for func, widget_type in widget_types.send(
            sender='get_wiget_types')]
        context['extra_scripts'] = [script for func, script in extra_js.send(
            sender='get_extra_js')]
        return context


class WidgetCreateView(LoginRequiredMixin, ActiveNavMixin, JSONResponseMixin, FormView):
    template_name = 'privatdash/widget_form.html'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        t = loader.get_template(self.template_name)
        c = Context({'form': form})
        json = {'html': t.render(c)}
        return self.render_json_response(json)

    def get_form_class(self):
        pk = self.request.GET.get('widget_type')
        form = None
        for func, widget_type in widget_types.send(sender='get_wiget_types'):
            if widget_type['pk'] == int(pk):
                form = widget_type['form']
                break
        return form

    def get_form_kwargs(self):
        kwargs = super(WidgetCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
