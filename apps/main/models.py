from django.utils.translation import ugettext as _
from django.db import models

from apps.utils.models import BaseModel


PROTOCOLS = [
    ('http', 'http'),
    ('https', 'https'),
]


class Site(BaseModel):
    title = models.CharField(_('Заголовок'), max_length=255)
    hostname = models.URLField(_('Hostname'), max_length=255)
    protocol = models.CharField(_('Протокол'), choices=PROTOCOLS, max_length=255)
    homepage_url = models.URLField(_('URL главной страницы'), max_length=255)

    is_available = models.BooleanField(_('Доступность сайта'))
    has_sitemap_xml = models.BooleanField(_('Есть карта сайта (XML)'))
    created_date = models.DateField(_('Дата создания сайта'), null=True)
    last_modified = models.CharField(_('Последнее обновление'), max_length=255, null=True)
    domain_expiration_date = models.DateField(_('Срок домена'), null=True)
    loading_speed = models.IntegerField(_('Скорость загрузки сайта'), default=0)
    weight = models.IntegerField(_('Вес сайта'), default=0)

    tls_version = models.CharField(_('SSL/TLS version'), max_length=255, null=True)
    os_version = models.CharField(_('Версия ОС'), max_length=255, null=True)
    os_warning = models.CharField(_('Предупреждения ОС'), max_length=5000, null=True)
    php_version = models.CharField(_('Версия PHP'), max_length=255, null=True)
    php_warning = models.CharField(_('Предупреждения PHP'), max_length=5000, null=True)
    web_server_version = models.CharField(_('Версия web сервера'), max_length=255, null=True)
    web_server_warning = models.CharField(_('Предупреждения web сервера'), max_length=5000, null=True)
    framework_name = models.CharField(_('Фреймворк/CMS'), max_length=255, null=True)
    framework_warning = models.CharField(_('Предупреждения фреймворка'), max_length=5000, null=True)

    total_links_count = models.IntegerField(_('Кол-во ссылок'), default=0)
    broken_links_count = models.IntegerField(_('Кол-во битых ссылок'), default=0)

    def __str__(self):
        return self.hostname

    class Meta:
        ordering = ['title']
        verbose_name = _('Сайт')
        verbose_name_plural = _('Сайты')
        db_table = 'sites'


class SiteVulnerabilities(BaseModel):
    site = models.ForeignKey(Site, models.CASCADE, 'vulnerabilities', verbose_name=_('Сайт'))
    text = models.CharField(_('Текст уязвимости'), max_length=5000, null=True)

    def __str__(self):
        return str(self.site_id) or 'n/a'

    class Meta:
        ordering = ['site_id']
        verbose_name = _('Уязвимость')
        verbose_name_plural = _('Уязвимости')
        db_table = 'site_vulnerabilities'


class SiteOpenPort(BaseModel):
    site = models.ForeignKey(Site, models.CASCADE, 'open_ports', verbose_name=_('Сайт'))
    port = models.IntegerField(_('Номер порта'))
    is_critical = models.BooleanField(_('Критично?'))
    warning_msg = models.CharField(_('Текст предупреждения'), max_length=1000)

    def __str__(self):
        return str(self.site_id) or 'n/a'

    class Meta:
        ordering = ['site_id']
        verbose_name = _('Открытый порт')
        verbose_name_plural = _('Открытые порты')
        db_table = 'site_open_ports'


class SiteBrokenLink(BaseModel):
    site = models.ForeignKey(Site, models.CASCADE, 'broken_links', verbose_name=_('Сайт'))
    path = models.CharField(_('path'), max_length=255)
    http_code = models.IntegerField(_('HTTP код'), default=404)

    def __str__(self):
        return str(self.site_id) or 'n/a'

    class Meta:
        ordering = ['site_id']
        verbose_name = _('Битая ссылка')
        verbose_name_plural = _('Битые ссылки')
        db_table = 'site_broken_links'


class SiteABTest(BaseModel):
    site = models.ForeignKey(Site, models.CASCADE, 'ab_tests', verbose_name=_('Сайт'))
    results_text = models.TextField(_('Результат ab теста (текст)'), max_length=5000)
    concurrency_level = models.IntegerField(_('Конкурентные потоки'), null=True)
    complete_requests = models.IntegerField(_('Кол-во направленные запросов'), null=True)
    time_taken = models.FloatField(_('Общее время выполнения'), null=True)
    failed_requests = models.IntegerField(_('Провальные запросы'), null=True)
    total_transferred = models.IntegerField(_('Загружено байтов'), null=True)
    html_transferred = models.IntegerField(_('Загружено байтов HTML'), null=True)

    requests_per_second = models.FloatField(_('Среднее кол-во запросов в секунду'), null=True)
    time_per_request = models.FloatField(_('Среднее время выполнения запроса [ms]'), null=True)
    time_per_request_2 = models.FloatField(_('Среднее время выполнения запроса по всем потокам [ms]'), null=True)
    transfer_rate = models.FloatField(_('Скорость загрузки [килобайт/сек]'), null=True)

    connection_time_min = models.FloatField(_('Время коннекта (мин.) [ms]'), null=True)
    connection_time_max = models.FloatField(_('Время коннекта (макс.) [ms]'), null=True)
    connection_time_avg = models.FloatField(_('Время коннекта (сред.) [ms]'), null=True)
    processing_time_min = models.FloatField(_('Время обработки (мин.) [ms]'), null=True)
    processing_time_max = models.FloatField(_('Время обработки (макс.) [ms]'), null=True)
    processing_time_avg = models.FloatField(_('Время обработки (сред.) [ms]'), null=True)
    waiting_time_min = models.FloatField(_('Время ожидания (мин.) [ms]'), null=True)
    waiting_time_max = models.FloatField(_('Время ожидания (макс.) [ms]'), null=True)
    waiting_time_avg = models.FloatField(_('Время ожидания (сред.) [ms]'), null=True)
    total_time_min = models.FloatField(_('Время ожидания (мин.) [ms]'), null=True)
    total_time_max = models.FloatField(_('Время ожидания (макс.) [ms]'), null=True)
    total_time_avg = models.FloatField(_('Время ожидания (сред.) [ms]'), null=True)

    def __str__(self):
        return str(self.site_id) or 'n/a'

    class Meta:
        ordering = ['site_id']
        verbose_name = _('AB тест')
        verbose_name_plural = _('AB тесты')
        db_table = 'site_ab_tests'
