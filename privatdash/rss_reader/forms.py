from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from privatdash.layout import Cancel, Row, Div

from .models import RSSSource

class RSSSourceCreateForm(forms.ModelForm):
    """Form to create a new RSSSource."""

    def __init__(self, user=None, *args, **kwargs):
        super(RSSSourceCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Field('title', wrapper_class='col-md-5 col-md-offset-1'),
                Field('source', wrapper_class='col-md-5'),
            ),
            Row(
                Field('description', wrapper_class='col-md-5 col-md-offset-1'),
                Field('categories', wrapper_class='col-md-5'),
                Field('user')
            ),
            Row(
            	Div(
	           		Submit('save', _('Save')),
               		Cancel(reverse('rss_reader_rsssource_list_view')),
               	    css_class='col-md-10, col-md-offset-1',
               	)
            )
        )

    class Meta:
        model = RSSSource
