from django.core.management.base import BaseCommand
from main.models import Site, SiteVulnerabilities

from .create_sites import execute
from json import loads


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = None

    def handle(self, *args, **options):
        for site in Site.objects.all():
            if SiteVulnerabilities.objects.filter(site=site).count() > 0:
                continue
            data = []
            if site.php_version:
                res = execute(f'searchsploit -j -c PHP {site.php_version}')
                data = loads(''.join(res[1]))["RESULTS_EXPLOIT"]
            if site.framework_name:
                res = execute(f'searchsploit -j -c {site.framework_name}')
                data.extend(loads(''.join(res[1]))["RESULTS_EXPLOIT"])
            if site.os_version:
                res = execute(f'searchsploit -j -c {site.os_version}')
                data.extend(loads(''.join(res[1]))["RESULTS_EXPLOIT"])
            for row in data:
                SiteVulnerabilities.objects.create(
                    site=site,
                    text=row['Title'],
                )
