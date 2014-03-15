from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML

from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from core.layout import Cancel, Row, Div

from core.forms import WidgetBaseForm

from .models import RSSSource, RSSCategory, RSSWidget


class RSSSourceForm(forms.ModelForm):
    """ Form to create or update a new RSSSource. """

    def __init__(self, user=None, *args, **kwargs):
        super(RSSSourceForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        if user:
            self.fields['user'].initial = user
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Field('title', wrapper_class='col-md-4 col-md-offset-2'),
                Field('source', wrapper_class='col-md-4'),
            ),
            Row(
                Field('categories', wrapper_class='col-md-8 col-md-offset-2'),
                Field('user')
            ),
            Row(
                Div(
                    Submit('save', _('Save')),
                    Cancel(reverse('rss_reader_rsssource_list_view')),
                    css_class='col-md-8, col-md-offset-2',
                )
            )
        )

    class Meta:
        model = RSSSource


class RSSCategoryForm(forms.ModelForm):
    """ Form to create or update a new Categoty. """

    def __init__(self, user=None, *args, **kwargs):
        super(RSSCategoryForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        if user:
            self.fields['user'].initial = user
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Field('title', wrapper_class='col-md-5 col-md-offset-1'),
                Field('user')
            ),
            Row(
                Div(
                    Submit('save', _('Save')),
                    Cancel(reverse('rss_reader_rsscategory_list_view')),
                    css_class='col-md-5 col-md-offset-1',
                )
            )
        )

    class Meta:
        model = RSSCategory


class RSSWidgetForm(WidgetBaseForm):
    """ Form to create a RSS Widget. """

    def __init__(self, user=None, *args, **kwargs):
        super(RSSWidgetForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.user:
            self.fields['sources'].queryset = RSSSource.objects.filter(user=self.user)
            self.fields['categories'].queryset = RSSCategory.objects.filter(user=self.user)
        self.fields['sources'].help_text = _('You can choose multiple entries by holding ctrl. '
            'If you leave this empty, all sources will be shown.')
        self.fields['categories'].help_text = _('You can choose multiple entries by holding '
            'ctrl. If you leave this empty, all categories will be shown.')
        self.helper = FormHelper()
        self.helper.form_action = reverse('rss_reader_rsswidget_create_view')
        self.helper.form_class = 'ajax'
        self.helper.form_id = 'widget-add-form'
        self.helper.form_method = 'post'
        self.helper.attrs['data-replace'] = '#widget-add-form'
        self.helper.layout = Layout(
                Field('title'),
                Field('only_new'),
                Field('num_of_entries'),
                Field('sources'),
                Field('categories'),
                HTML('{% load i18n %}<button type="button" class="btn btn-default" data-dismiss="modal">{% trans "Cancel" %}</button>'),
                Submit('save', _('Add'), wrapper_class="btn btn-primary")
        )

    def save(self, *args, **kwargs):
        instance = super(RSSWidgetForm, self).save(*args, **kwargs)
        Widget.objects.create(user=self.user, widget_type=instance)
        return instance

    class Meta:
        model = RSSWidget

