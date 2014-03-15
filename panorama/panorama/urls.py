from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'panorama.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^rss_reader/', include('rss_reader.urls')),
    url(r'^staticwidgets/', include('staticwidgets.urls')),
    url(r'^accounts/', include('panorama.registration_urls')),
    url(r'^', include('core.urls')),
)
