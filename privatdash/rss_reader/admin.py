from django.contrib import admin

from .models import RSSSource, RSSEntry, RSSWidget, RSSCategory

# Register your models here.
admin.site.register(RSSCategory)
admin.site.register(RSSSource)
admin.site.register(RSSEntry)
admin.site.register(RSSWidget)
