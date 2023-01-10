""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: записывает все адреса в приложении: users
Переменные:
 - urlpatterns: список адресов
"""
from django.urls import path, include


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
