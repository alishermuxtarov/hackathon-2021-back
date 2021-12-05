from django.contrib import admin

from .models import Site, SiteVulnerabilities, SiteOpenPort, SiteBrokenLink, SiteABTest


class SiteVulnerabilitiesInline(admin.TabularInline):
    model = SiteVulnerabilities
    fields = ['text']
    extra = 1


class SiteOpenPortInline(admin.TabularInline):
    model = SiteOpenPort
    fields = ['port', 'is_critical', 'warning_msg']
    extra = 1


class SiteBrokenLinkInline(admin.TabularInline):
    model = SiteBrokenLink
    fields = ['path', 'http_code']
    extra = 1


@admin.register(SiteABTest)
class SiteABTestAdmin(admin.ModelAdmin):
    fields = [
        'site',
        'results_text',
        'concurrency_level',
        'complete_requests',
        'time_taken',
        'failed_requests',
        'total_transferred',
        'html_transferred',

        'requests_per_second',
        'time_per_request',
        'time_per_request_2',
        'transfer_rate',

        'connection_time_min',
        'connection_time_max',
        'connection_time_avg',
        'processing_time_min',
        'processing_time_max',
        'processing_time_avg',
        'waiting_time_min',
        'waiting_time_max',
        'waiting_time_avg',
        'total_time_min',
    ]
    list_display = [
        'site_id',
        'site',
        'requests_per_second',
        'concurrency_level',
        'time_taken'
    ]
    list_display_links = ['site']
    ordering = ['id']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'hostname',
        'protocol',
        'homepage_url',

        'is_available',
        'has_sitemap_xml',
        'created_date',
        'last_modified',
        'domain_expiration_date',
        'loading_speed',
        'weight',

        'tls_version',
        'os_version',
        'os_warning',
        'php_version',
        'php_warning',
        'web_server_version',
        'web_server_warning',
        'framework_name',
        'framework_warning',

        'total_links_count',
        'broken_links_count',
    ]
    list_display_links = ['id']
    list_display = ['id', 'title', 'hostname']
    ordering = ['id']
    inlines = [SiteVulnerabilitiesInline, SiteBrokenLinkInline, SiteOpenPortInline]
