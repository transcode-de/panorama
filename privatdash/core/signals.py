from django.dispatch import Signal


side_navigation = Signal(providing_args=['request'])
extra_js = Signal(providing_args=['request'])
extra_css = Signal(providing_args=['request'])
widget_types = Signal(providing_args=['request'])
