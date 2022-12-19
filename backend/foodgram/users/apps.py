""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

apps.py -> настройки конфигурации приложения: users
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Method required when the User application is created."""
    name = 'users'