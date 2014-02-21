# encoding: utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Div, HTML


class Row(Div):
    """Bootstrap row class."""
    css_class = 'row'


class Cancel(HTML):
    """Cancels the operation."""
    def __init__(self, url):
        """Redirects to the given url."""
        html = '<a href="%s">Abbrechen</a>' % url
        super(Cancel, self).__init__(html)
