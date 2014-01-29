from django.conf.urls import patterns, url

from .views import (RSSReaderView, RSSSourceListView, RSSSourceCreateView, RSSSourceUpdateView,
    RSSSourceDeleteView, RSSCategoryListView, RSSCategoryCreateView, RSSCategoryUpdateView,
    RSSCategoryDeleteView)


urlpatterns = patterns('',
    url(r'^$', RSSReaderView.as_view(), name='rss_reader_view'),
    url(r'^rss_source/list/$', RSSSourceListView.as_view(), name='rss_reader_rsssource_list_view'),
    url(r'^rss_source/add/$', RSSSourceCreateView.as_view(), name='rss_reader_rsssource_create_view'),
    url(r'^rss_source/update/(?P<pk>\d+)$', RSSSourceUpdateView.as_view(),
        name='rss_reader_rsssource_update_view'),
    url(r'^rss_source/delete/(?P<pk>\d+)$', RSSSourceDeleteView.as_view(),
        name='rss_reader_rsssource_delete_view'),

    url(r'^rss_category/list/$', RSSCategoryListView.as_view(), name='rss_reader_rsscategory_list_view'),
    url(r'^rss_category/add/$', RSSCategoryCreateView.as_view(), name='rss_reader_rsscategory_create_view'),
    url(r'^rss_category/update/(?P<pk>\d+)$', RSSCategoryUpdateView.as_view(),
        name='rss_reader_rsscategory_update_view'),
    url(r'^rss_category/delete/(?P<pk>\d+)$', RSSCategoryDeleteView.as_view(),
        name='rss_reader_rsscategory_delete_view'),
)
