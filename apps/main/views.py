from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .serializers import SiteSerializer, SiteListSerializer, SiteVulnerabilitiesSerializer, SiteBrokenLinkSerializer, \
    SiteABTestSerializer
from .models import Site, SiteVulnerabilities, SiteBrokenLink, SiteABTest


class SiteListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SiteListSerializer

    def get_queryset(self):
        return Site.objects.all()


class SiteDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SiteSerializer

    def get_queryset(self):
        return Site.objects.all()


class SiteVulnerabilitiesListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SiteVulnerabilitiesSerializer

    def get_queryset(self):
        return SiteVulnerabilities.objects.all()


class SiteBrokenLinkListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SiteBrokenLinkSerializer

    def get_queryset(self):
        return SiteBrokenLink.objects.all()


class SiteABTestListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SiteABTestSerializer

    def get_queryset(self):
        return SiteABTest.objects.all()

