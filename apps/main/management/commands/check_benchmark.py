from traceback import print_exc

from django.core.management.base import BaseCommand
from main.models import Site, SiteABTest

from .create_sites import execute


class Command(BaseCommand):
    def handle(self, *args, **options):
        for site in Site.objects.all():
            if SiteABTest.objects.filter(site=site).exists():
                continue
            try:
                results = self.get_results(site.homepage_url)
                if results:
                    SiteABTest.objects.create(site=site, **results)
            except Exception as msg:
                print(f'[{site.hostname}]: {msg}')
                print_exc()

    @staticmethod
    def get_results(site):
        res = execute(f'ab -c 10 -n 100 {site}')
        if res[2] is not True:
            return dict()
        result = '\n'.join(res[1])

        def get(key):
            return result.split(key + ':')[1].split()[0].strip()

        def get_times(key, index):
            d = [s for s in result.split('\n') if key in s][-1]
            return d.split(key + ':')[1].split()[index].strip()

        def get_across_all():
            d = [s for s in result.split('\n') if 'Time per request:' in s][-1]
            return d.split(':')[1].split()[0].strip()

        return dict(
            results_text=result,
            concurrency_level=get('Concurrency Level'),
            complete_requests=get('Complete requests'),
            time_taken=get('Time taken for tests'),
            failed_requests=get('Failed requests'),
            total_transferred=get('Total transferred'),
            html_transferred=get('HTML transferred'),
            requests_per_second=get('Requests per second'),
            time_per_request=get('Time per request'),
            time_per_request_2=get_across_all(),
            transfer_rate=get('Transfer rate'),
            connection_time_min=get_times('Connect', 0),
            connection_time_max=get_times('Connect', 1),
            connection_time_avg=get_times('Connect', 2),
            processing_time_min=get_times('Processing', 0),
            processing_time_max=get_times('Processing', 1),
            processing_time_avg=get_times('Processing', 2),
            waiting_time_min=get_times('Waiting', 0),
            waiting_time_max=get_times('Waiting', 1),
            waiting_time_avg=get_times('Waiting', 2),
            total_time_min=get_times('Total', 0),
            total_time_max=get_times('Total', 1),
            total_time_avg=get_times('Total', 2),
        )
