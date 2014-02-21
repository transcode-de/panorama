from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'privatdash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^rss_reader/', include('rss_reader.urls')),
    url(r'^accounts/', include('privatdash.registration_urls')),
    url(r'^', include('core.urls')),
)
