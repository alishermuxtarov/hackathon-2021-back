try:
    from config.settings.general import *
except ImportError:
    pass


WSGI_APPLICATION = 'config.wsgi.admin.application'
ROOT_URLCONF = 'config.urls.admin'
