from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from core.forms import WidgetBaseForm

from .models import WeatherWidget, TextWidget



class WeatherWidgetForm(WidgetBaseForm):
    """ Form to create a RSS Widget. """

    def __init__(self, user=None, *args, **kwargs):
        super(WeatherWidgetForm, self).__init__(*args, **kwargs)
        self.user = user
        self.helper = FormHelper()
        self.helper.form_action = reverse('staticwidgets_weatherwidget_create_view')
        self.helper.form_class = 'ajax'
        self.helper.form_id = 'widget-add-form'
        self.helper.form_method = 'post'
        self.helper.attrs['data-replace'] = '#widget-add-form'
        self.helper.layout = Layout(
                Field('title'),
                Field('location'),
                HTML('{% load i18n %}<button type="button" class="btn btn-default" data-dismiss="modal">{% trans "Cancel" %}</button>'),
                Submit('save', _('Add'), wrapper_class="btn btn-primary")
        )

    class Meta:
        model = WeatherWidget


class TextWidgetForm(WidgetBaseForm):
    """ Form to create a Text Widget. """

    def __init__(self, user=None, *args, **kwargs):
        super(TextWidgetForm, self).__init__(*args, **kwargs)
        self.user = user
        self.helper = FormHelper()
        self.helper.form_action = reverse('staticwidgets_textwidget_create_view')
        self.helper.form_class = 'ajax'
        self.helper.form_id = 'widget-add-form'
        self.helper.form_method = 'post'
        self.helper.attrs['data-replace'] = '#widget-add-form'
        self.helper.layout = Layout(
                Field('title'),
                Field('text'),
                HTML('{% load i18n %}<button type="button" class="btn btn-default" data-dismiss="modal">{% trans "Cancel" %}</button>'),
                Submit('save', _('Add'), wrapper_class="btn btn-primary")
        )

    class Meta:
        model = TextWidget
