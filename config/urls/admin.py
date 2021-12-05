from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'Панель администратора'

urlpatterns = [
    path('admin/', admin.site.urls),
]
