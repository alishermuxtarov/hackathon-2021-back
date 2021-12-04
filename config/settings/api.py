try:
    from config.settings.general import *
except ImportError:
    pass


WSGI_APPLICATION = 'config.wsgi.api.application'
ROOT_URLCONF = 'config.urls.api'
