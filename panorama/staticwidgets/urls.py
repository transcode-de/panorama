from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^weather_widget/add/$', views.WeatherWidgetCreateView.as_view(),
        name='staticwidgets_weatherwidget_create_view')
)
