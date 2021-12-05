from django.core.management.base import BaseCommand
from main.models import Site


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = None

    def handle(self, *args, **options):
        for site in Site.objects.all():
            pass
