from traceback import print_exc

from django.core.management.base import BaseCommand
from main.models import Site, SiteOpenPort

from .create_sites import execute

ALLOWED_PORTS = ['25', '80', '443', '53', '953']

RESULT = '''
Starting Nmap 7.70 ( https://nmap.org ) at 2021-12-05 13:59 +05
Nmap scan report for www.tashkent.uz (213.230.91.84)
Host is up (0.0022s latency).
rDNS record for 213.230.91.84: mail.tashkent.uz
Not shown: 924 filtered ports, 65 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
25/tcp   open  smtp
80/tcp   open  http
110/tcp  open  pop3
143/tcp  open  imap
443/tcp  open  https
465/tcp  open  smtps
993/tcp  open  imaps
995/tcp  open  pop3s
7025/tcp open  vmsvc-2
8443/tcp open  https-alt

Nmap done: 1 IP address (1 host up) scanned in 47.21 seconds
'''


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
