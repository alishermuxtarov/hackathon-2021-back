from traceback import print_exc

from django.core.management.base import BaseCommand
from main.models import Site, SiteOpenPort

from .create_sites import execute

ALLOWED_PORTS = ['25', '80', '443', '53', '953']


class Command(BaseCommand):
    def handle(self, *args, **options):
        for site in Site.objects.all():
            if SiteOpenPort.objects.filter(site=site).count() > 0:
                continue
            try:
                print(site.hostname)
                results = self.get_results(site.hostname)
                for result in results:
                    SiteOpenPort.objects.create(site=site, **result)
            except Exception as msg:
                print(f'[{site.hostname}]: {msg}')
                print_exc()

    @staticmethod
    def get_results(site):
        res = execute(f'nmap -sS -T4 -Pn {site}')
        if res[2] is not True:
            return []
        result = '\n'.join(res[1])

        results = [r for r in result.split('\n') if 'open' in r.split()]
        data = []
        for result in results:
            a, b, c = result.split()
            port = a.split('/')[0].strip()
            msg, is_critical = '', False
            if port not in ALLOWED_PORTS:
                is_critical = True
                msg = f'Сервис "{c}" должен быть скрыт за корпоративный VPN.'

            data.append(dict(
                port=port,
                is_critical=is_critical,
                warning_msg=msg,
            ))
        return data
