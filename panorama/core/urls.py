from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
	url(r'^$', views.Dashboard.as_view(), name='dashboard'),
	url(r'^widget/create/$', views.WidgetCreateView.as_view(), name='widget_create'),
	url(r'^widget/reload/(?P<pk>\d+)$', views.WidgetReloadView.as_view(),
		name='widget_reload')
)
