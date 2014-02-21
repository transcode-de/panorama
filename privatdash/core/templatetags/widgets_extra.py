from django import template
from django.contrib.auth import get_user_model

register = template.Library()

from ..models import Widget


def render_widget(user_pk, widget_pk):
    widget = Widget.objects.get(pk=widget_pk)
    user = get_user_model().objects.get(pk=user_pk)
    return widget.widget_type.render(user)


register.assignment_tag(render_widget)
