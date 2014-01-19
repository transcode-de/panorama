from django.conf.urls import patterns, url

from .views import RSSReaderView, RSSSourceListView


urlpatterns = patterns('',
    url(r'^$', RSSReaderView.as_view(), name='rss_reader_view'),
    url(r'^list/$', RSSSourceListView.as_view(), name='rss_reader_rsssource_list_view'),
)
