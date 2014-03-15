from django.contrib.contenttypes.models import ContentType

from django.dispatch import receiver

from core.signals import widget_types, extra_js

from .models import WeatherWidget, TextWidget
from .forms import WeatherWidgetForm, TextWidgetForm


@receiver(widget_types, dispatch_uid="widget_types_weather_widget")
def widget_types_weather_widget(sender, **kwargs):
    ct = ContentType.objects.get_for_model(WeatherWidget)
    return {
        'pk': ct.pk,
        'name': 'Weather Widget',
        'form': WeatherWidgetForm
    }


@receiver(widget_types, dispatch_uid="widget_types_text_widget")
def widget_types_text_widget(sender, **kwargs):
    ct = ContentType.objects.get_for_model(TextWidget)
    return {
        'pk': ct.pk,
        'name': 'Static Text Widget',
        'form': TextWidgetForm
    }


@receiver(extra_js, dispatch_uid="extra_js_weather_widgets")
def extra_js_weather_widgets(sender, **kwargs):
    return ['js/vendor/openWeather.min.js', 'js/weather_widget.js']
