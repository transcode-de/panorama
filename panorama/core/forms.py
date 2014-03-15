from django import forms

from .models import Widget


class WidgetBaseForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        instance = super(WidgetBaseForm, self).save(*args, **kwargs)
        Widget.objects.create(user=self.user, widget_type=instance)
        return instance
