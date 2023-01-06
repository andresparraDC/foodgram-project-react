""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: Он регистрирует список адресов в Django.
Переменные:
 - urlpatterns -> список адресов
"""
from django.contrib import admin

from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #
    path('', include('foodgram_app.urls', namespace='foodgram_app')),
    #
    path('admin/', admin.site.urls),
    #
    path('auth/', include('users.urls', namespace='users')),
    #
    path('auth/', include('django.contrib.auth.urls')),
    #
    path('about/', include('about.urls', namespace='about')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
