from django.conf.urls import patterns, url

from .views import RSSReaderView, RSSSourceListView, RSSSourceAddView


urlpatterns = patterns('',
    url(r'^$', RSSReaderView.as_view(), name='rss_reader_view'),
    url(r'^rss_source/list/$', RSSSourceListView.as_view(), name='rss_reader_rsssource_list_view'),
    url(r'^rss_source/add/$', RSSSourceAddView.as_view(), name='rss_reader_rsssource_create_view'),
)
