from django.contrib import admin
from django.urls import path, re_path

from menu.views import menu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_named_url/', menu, name='named_url'),  # Для демонстрации.
    re_path(r'^(.*)', menu, name='menu'),
]
