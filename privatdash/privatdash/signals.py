from django.dispatch import Signal


side_navigation = Signal(providing_args=['request'])
additional_js = Signal(providing_args=['request'])
additional_css = Signal(providing_args=['request'])
