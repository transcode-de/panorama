from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from rss_reader.models import RSSSource


class Command(BaseCommand):
    help = 'Update all feeds. There last update musst be older than 1h.'

    def handle(self, *args, **options):
        time_threshold = now() - timedelta(hours=1)
        sources = RSSSource.objects.filter(updated__lt=time_threshold)
        num_of_sources = sources.count()
        if num_of_sources:
            for source in sources:
            	source.save()
            	self.stdout.write('Updated %s.' % source)
            self.stdout.write('------------------------------------------')
            self.stdout.write('Updated %i RSS sources.' % num_of_sources)
        else:
            self.stdout.write('All sources up to date.')
