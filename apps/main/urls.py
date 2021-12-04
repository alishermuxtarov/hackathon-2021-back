from django.urls import path

from .views import SiteListView, SiteDetailView, SiteVulnerabilitiesListView, SiteBrokenLinkListView, SiteABTestListView

urlpatterns = [
    path('sites/', SiteListView.as_view(), name='sites.list'),
    path('sites/<int:pk>/', SiteDetailView.as_view(), name='sites.detail'),
    path('vulnerabilities/', SiteVulnerabilitiesListView.as_view(), name='vulnerabilities.list'),
    path('broken_links/', SiteBrokenLinkListView.as_view(), name='broken_links.list'),
    path('ab_tests/', SiteABTestListView.as_view(), name='ab_tests.list'),
]
