from urllib.parse import urljoin

from rest_framework import serializers

from .models import Site, SiteVulnerabilities, SiteOpenPort, SiteBrokenLink, SiteABTest


class SiteVulnerabilitiesSerializer(serializers.ModelSerializer):
    site_hostname = serializers.CharField(source='site.hostname')

    class Meta:
        model = SiteVulnerabilities
        fields = ['site_hostname', 'text']


class SiteOpenPortSerializer(serializers.ModelSerializer):
    site_hostname = serializers.CharField(source='site.hostname')

    class Meta:
        model = SiteOpenPort
        fields = ['site_hostname', 'port', 'is_critical', 'warning_msg']


class SiteBrokenLinkSerializer(serializers.ModelSerializer):
    site_hostname = serializers.CharField(source='site.hostname')
    url = serializers.SerializerMethodField()

    def get_url(self, broken_link):
        return urljoin(broken_link.site.hostname, broken_link.path)

    class Meta:
        model = SiteBrokenLink
        fields = ['site_hostname', 'path', 'url', 'http_code']


class SiteABTestSerializer(serializers.ModelSerializer):
    site_hostname = serializers.CharField(source='site.hostname')

    class Meta:
        model = SiteABTest
        fields = [
            'site_hostname',
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


class SiteSerializer(serializers.ModelSerializer):
    vulnerabilities = SiteVulnerabilitiesSerializer(many=True)
    open_ports = SiteOpenPortSerializer(many=True)
    broken_links = SiteBrokenLinkSerializer(many=True)
    ab_tests = SiteABTestSerializer(many=True)

    class Meta:
        model = Site
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

            'vulnerabilities',
            'open_ports',
            'broken_links',
            'ab_tests',
        ]


class SiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
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

            'vulnerabilities',
            'open_ports',
            'broken_links',
        ]
