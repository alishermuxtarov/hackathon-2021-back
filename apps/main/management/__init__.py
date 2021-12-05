from django.core.management.base import BaseCommand

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


class MailCommand(BaseCommand):

    def handle(self, *args, **options):
        pass
