from subprocess import Popen, STDOUT, PIPE, TimeoutExpired
from urllib.parse import urlparse
from datetime import datetime
from math import ceil
from os import system

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from main.models import Site
from grab import Grab


sites = [
    'http://sovminrk.gov.uz/',
    'http://andijan.uz',
    'https://www.buxoro.uz',
    'https://www.jizzax.uz',
    'https://www.qashqadaryo.uz',
    'https://navoi.uz/index.php?/uz',
    'https://www.namangan.uz/uz/',
    'https://samarkand.uz',
    'https://www.surxondaryo.uz/uz',
    'http://sirdaryo.uz/oz',
    'http://www.tashvil.gov.uz',
    'https://fergana.uz/index.php?/',
    'https://www.xorazm.uz',
    'https://www.tashkent.uz'
]


def execute(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    try:
        outs, errs = p.communicate(timeout=600)
    except TimeoutExpired:
        p.kill()
        return ['', 'timeout', False]

    return [errs, outs.decode('utf-8').strip().split('\n'), p.returncode == 0]


class Command(BaseCommand):

    def handle(self, *args, **options):
        g = Grab()
        for site in sites:
            p = urlparse(site)
            is_available = system(f'curl -s {site} > /dev/null') == 0
            site_map_url = f'https://{p.netloc}/sitemap.xml'
            g.go(site_map_url)
            has_sitemap_xml = g.doc.code == 200

            g.go(site)
            title = g.doc.select('//title').text()

            res = execute(f"whois {p.netloc} | grep created")
            domain_expiration_date = None
            if res[2] is True:
                date = res[1][0].split(':')[-1].strip()
                date = datetime.strptime(date, '%Y-%m-%d')
                n = now()
                year = n.year
                if date.month < n.month:
                    year = n.year + 1
                dt_str = f'{year}-{date.month}-{date.day}'
                domain_expiration_date = datetime.strptime(dt_str, '%Y-%m-%d')

            res = execute("curl -s -w '%{time_total}\n' -o/dev/null " + site)
            loading_speed = 0
            if res[2] is True:
                loading_speed = ceil(float(res[1][0]))

            res = execute("curl -s -w '%{size_download}\n' -o/dev/null " + site)
            weight = 0
            if res[2] is True:
                weight = res[1][0]

            res = execute(f"curl -s -v -I -L {site} 2>&1|grep TLSv|tail -1")
            tls_version = 0
            if res[2] is True:
                try:
                    tls_version = res[1][0].split('TLSv')[1].split()[0]
                except:
                    pass
            if Site.objects.filter(hostname=p.netloc).exists():
                Site.objects.filter(hostname=p.netloc).update(
                    title=title,
                    hostname=p.netloc,
                    protocol=p.scheme,
                    homepage_url=site,
                    is_available=is_available,
                    has_sitemap_xml=has_sitemap_xml,
                    created_date=now(),
                    last_modified=now(),
                        domain_expiration_date=domain_expiration_date,
                    loading_speed=loading_speed,
                    weight=weight,
                    tls_version=tls_version,
                )
            else:
                Site.objects.create(
                    title=title,
                    hostname=p.netloc,
                    protocol=p.scheme,
                    homepage_url=site,
                    is_available=is_available,
                    has_sitemap_xml=has_sitemap_xml,
                    created_date=now(),
                    last_modified=now(),
                    domain_expiration_date=domain_expiration_date,
                    loading_speed=loading_speed,
                    weight=weight,
                    tls_version=tls_version,
                )
