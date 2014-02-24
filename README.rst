panorama
==========

panorama is a open source dashboard applikation. It allows you to create a dashboard with several widgets about the information you want to see at the first view. It has also kind of a plugin system to create your own widgets.

setup
=====

testing
=======

writing your own widgets
========================

The plugin system is based on django signals. With some small receivers, you are able to put your stuff into the application.

sidenav
-------

If you want to extend the sidenavigation, you have to listen to the react on the `side_navigation` signal.

You just have to make sure to return a dictionary with elements:

* active_name: this value allows you to set the navigation element to active, if you use the `ActiveNavMixin`
* icon_classes: these css classes will be set to generate a icon. You are able to use `Glyphicons from bootstrap
<http://getbootstrap.com/components/#glyphicons>`_ or `FontAwesome <http://fontawesome.io/icons/>`_
* title: the text shown in the sidenav
* url: the url, the link of the sidenav element should open

Here is the example from the rss_reader app:

    :::Python
        from core.signals import side_navigation

        @receiver(side_navigation, dispatch_uid="side_navigation_rss_reader")
        def side_navigation_rss_reader(sender, **kwargs):
            return {
                'active_name': 'rss_reader',
                'icon_classes': 'fa fa-rss',
                'title': _('RSS Reader'),
                'url': reverse('rss_reader_view'),
            }

In the sidenav, it will be rendered like this:

    :::

        {% for sidenav_element in sidenav_elements %}
        <li>
            <i class="{{ sidenav_element.icon_classes }} {% if sidenav_active == sidenav_element.active_name %}active{% endif %}"></i>
            <a href="{{ sidenav_element.url }}" class="app-title">{{ sidenav_element.title}}</a>
        </li>
        {% endfor %}

If you want it to be the active sidenav element, you can use the `ActiveNavMixin`. Just let you view inherit from it and set the `sidenav_active` variable. Here is a short example out of the rss_reader app:

    :::Python
        from core.views import ActiveNavMixin


        class RSSReaderBaseView(LoginRequiredMixin, ActiveNavMixin):
            sidenav_active = 'rss_reader'


        class RSSReaderDisplayBaseView(RSSReaderBaseView):
            [...]


	    class RSSReaderView(RSSReaderDisplayBaseView, ListView):
            [...]
