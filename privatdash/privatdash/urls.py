from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import Dashboard

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'privatdash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', Dashboard.as_view(), name='dashboard'),
    url(r'^rss_reader/$', include('rss_reader.urls'))
)
