from django.conf import settings

def sidenav(request):
    return {'sidenav_elements': settings.NAV_INCLUDE_TEMPLATES}
