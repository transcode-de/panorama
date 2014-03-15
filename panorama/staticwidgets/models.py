from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _

from core.signals import widget_types, extra_js


class WeatherWidget(models.Model):
    TEMPLATE_NAME = 'staticwidgets/weather_widget.html'
    ICON_CLASS = 'fa fa-cloud'
    WIDGET_CLASS = 'weather-widget'

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    location = models.CharField(max_length=200, verbose_name=_('Location'))

    class Meta:
        verbose_name = _('Weather Widget')
        verbose_name_plural = _('Weather Widgets')

    def render(self, user, widget_pk):
        t = loader.get_template(self.TEMPLATE_NAME)
        c = Context({
            'object': self,
            'widget_pk': widget_pk,
        })
        return t.render(c)


class TextWidget(models.Model):
    TEMPLATE_NAME = 'staticwidgets/text_widget.html'
    ICON_CLASS = 'fa fa-align-justify '
    WIDGET_CLASS = 'text-widget'

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    text = models.CharField(max_length=2000, verbose_name=_('Text'))

    class Meta:
        verbose_name = _('Text Widget')
        verbose_name_plural = _('Text Widgets')

    def render(self, user, widget_pk):
        t = loader.get_template(self.TEMPLATE_NAME)
        c = Context({
            'object': self,
            'widget_pk': widget_pk
        })
        return t.render(c)


@receiver(widget_types, dispatch_uid="widget_types_weather_widget")
def widget_types_weather_widget(sender, **kwargs):
    ct = ContentType.objects.get_for_model(WeatherWidget)
    return {
        'pk': ct.pk,
        'name': 'Weather Widget',
        'form': 'staticwidgets.forms.WeatherWidgetForm'
    }


@receiver(widget_types, dispatch_uid="widget_types_text_widget")
def widget_types_text_widget(sender, **kwargs):
    ct = ContentType.objects.get_for_model(TextWidget)
    return {
        'pk': ct.pk,
        'name': 'Static Text Widget',
        'form': 'staticwidgets.forms.TextWidgetForm'
    }


@receiver(extra_js, dispatch_uid="extra_js_weather_widgets")
def extra_js_weather_widgets(sender, **kwargs):
    return ['js/vendor/openWeather.min.js', 'js/weather_widget.js']
