""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: Он регистрирует список адресов в Django.
Переменные:
 - urlpatterns -> список адресов
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('foodgram_app.urls')),
    path('api/', include('users.urls')),
]
