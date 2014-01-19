from django.conf.urls import patterns, url

from .views import RSSReaderView


urlpatterns = patterns('',
    url(r'^$', RSSReaderView.as_view(), name='rss_reader_view'),
)
