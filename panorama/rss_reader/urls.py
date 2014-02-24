from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.RSSReaderView.as_view(), name='rss_reader_view'),
    url(r'^rss_source/list/$', views.RSSSourceListView.as_view(), name='rss_reader_rsssource_list_view'),
    url(r'^rss_source/add/$', views.RSSSourceCreateView.as_view(), name='rss_reader_rsssource_create_view'),
    url(r'^rss_source/update/(?P<pk>\d+)$', views.RSSSourceUpdateView.as_view(),
        name='rss_reader_rsssource_update_view'),
    url(r'^rss_source/delete/(?P<pk>\d+)$', views.RSSSourceDeleteView.as_view(),
        name='rss_reader_rsssource_delete_view'),

    url(r'rss_entry/mark_read/(?P<pk>\d+)$', views.RSSEntryMarkReadView.as_view(),
        name='rss_entry_mark_read'),

    url(r'^rss_category/list/$', views.RSSCategoryListView.as_view(), name='rss_reader_rsscategory_list_view'),
    url(r'^rss_category/add/$', views.RSSCategoryCreateView.as_view(), name='rss_reader_rsscategory_create_view'),
    url(r'^rss_category/update/(?P<pk>\d+)$', views.RSSCategoryUpdateView.as_view(),
        name='rss_reader_rsscategory_update_view'),
    url(r'^rss_category/delete/(?P<pk>\d+)$', views.RSSCategoryDeleteView.as_view(),
        name='rss_reader_rsscategory_delete_view'),

    url(r'^rss_widget/add/$', views.RSSWidgetCreateView.as_view(), name='rss_reader_rsswidget_create_view')
)
