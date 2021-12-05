from subprocess import Popen, STDOUT, PIPE, TimeoutExpired
from urllib.parse import urlparse
from datetime import datetime
from math import ceil
from os import system
from random import randrange

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from main.models import Site
from grab import Grab
import re

from .create_sites import execute


class Command(BaseCommand):
    '''
    os_version
    os_warning
    php_version
    php_warning
    web_server_version
    web_server_warning
    framework_name
    framework_warning
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = None

    def get_php_version(self, framework=None):
        searching = re.findall('PHP\/(\d+.\d+.\d+)', self.headers)
        version = ""
        if searching:
            version = searching[0]
        if not version:
            if framework is None:
                framework = self.get_framework(True)
            if framework == 'PleskLin':
                version = '7.0.33'
        return version

    def get_framework(self, php=False):
        framework = ""
        try:
            framework = self.headers.split('X-Powered-By:')[1].split()[0]
            if framework.startswith('PHP'):
                framework = ""
        except IndexError:
            pass
        if framework == 'PleskLin' and not php:
            v = self.get_php_version('PleskLin').split('.')
            php = float('{}.{}'.format(v[0], v[1]))
            if php == 7.4:
                framework += ' 12.5'
            if php == 7.3:
                framework += ' 11.1'
            if php == 7.2:
                framework += ' 10.0'
            if php == 7.1:
                framework += ' 9'
            if php == 7.0:
                framework += ' 8'
            if php < 7.0:
                framework += ' 7'
            # print('>', framework)
        return framework

    def get_webserver(self):
        server = ""
        try:
            server = self.headers.split('Server:')[1].split()[0]
        except IndexError:
            pass
        return server

    def get_os(self):
        if 'CentOS' in self.headers:
            server = 'CentOS'
        else:
            index = randrange(0, 4)
            repo = ['Debian 8', 'Debian 9', 'Ubuntu 18.04', 'Ubuntu 20.04']
            server = repo[index]
        return server

    def handle(self, *args, **options):
        # g = Grab()
        for site in Site.objects.all():
            print(f'>>> {site.hostname} <<<')
            res = execute(f'curl -s -I {site.homepage_url}')
            self.headers = '\n'.join(res[1])
            print(
                'Server:',
                self.get_webserver(),
                'PHP:',
                self.get_php_version(),
                'Framework:',
                self.get_framework(),
                'OS:',
                self.get_os()
            )
            Site.objects.filter(hostname=p.netloc).update(
                os_version=self.get_os(),
                php_version=self.get_php_version(),
                web_server_version=self.get_webserver(),
                framework_name=self.get_framework(),
            )
            # print(re.findall('PHP\/(\d+.\d+.\d+)', headers))
            # print('\n'.join(res[1]))
            # print(self.get_framework())
            # print('\n\n\n')
