from config.urls.api import urlpatterns as api_urlpatterns
from .admin import urlpatterns as admin_urlpatterns

urlpatterns = api_urlpatterns + admin_urlpatterns
