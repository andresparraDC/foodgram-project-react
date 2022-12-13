"""
Спринт 14
Проект: 
Автор: Фредди Андрес Парра

Имя файла: urls.py
Описание файла: Он регистрирует список адресов в Django.
Переменные:
 - urlpatterns -> список адресов
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('foodgram_app.urls', namespace='foodgram_app')),
    path('admin/', admin.site.urls),
]
