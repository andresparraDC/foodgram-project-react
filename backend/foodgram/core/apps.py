""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

apps.py -> настройки конфигурации приложения: core
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Method required when the Core application is created."""
    name = 'core'