""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: записывает все адреса в приложении: users
Переменные:
 - urlpatterns: список адресов
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import UsersViewSet

# router_v1 = DefaultRouter()
# router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]