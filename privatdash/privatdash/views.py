from braces.views import LoginRequiredMixin

from django.views.generic import TemplateView


class ActiveNavMixin(object):
    sidenav_active = 'dashboard'

    def get_context_data(self, *args, **kwargs):
        context = super(ActiveNavMixin, self).get_context_data(*args, **kwargs)
        context['sidenav_active'] = self.sidenav_active
        return context


class Dashboard(LoginRequiredMixin, ActiveNavMixin, TemplateView):
	template_name = 'privatdash/dashboard.html'
