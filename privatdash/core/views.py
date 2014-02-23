from braces.views import LoginRequiredMixin, JSONResponseMixin

from django.template import loader, Context
from django.views.generic import ListView, FormView, View


from .models import Widget
from .signals import widget_types, extra_js, extra_css
from .templatetags.widgets_extra import render_widget


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

        extra_scripts = []
        all_extra_scripts = [scripts for func, scripts in extra_js.send(sender='get_extra_js')]
        for app_scripts in all_extra_scripts:
            for script in app_scripts:
                extra_scripts.append(script)
        context['extra_scripts'] = extra_scripts

        extra_styles = []
        all_extra_styles = [styles for func, styles in extra_css.send(sender='get_extra_css')]
        for app_style in all_extra_styles:
            for style in app_style:
                extra_styles.append(style)
        context['extra_styles'] = extra_styles
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


class WidgetReloadView(LoginRequiredMixin, JSONResponseMixin, View):

    def get(self, *args, **kwargs):
        user_pk = self.request.user.pk
        widget_pk = self.kwargs.get('pk')
        return self.render_json_response({'html': render_widget(user_pk, widget_pk)})
