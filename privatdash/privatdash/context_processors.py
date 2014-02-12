from .signals import side_navigation


def sidenav(request):
    sidenav_elements = [nav_element for func, nav_element in side_navigation.send(sender='get_sidenavs')]
    return {'sidenav_elements': sidenav_elements}
