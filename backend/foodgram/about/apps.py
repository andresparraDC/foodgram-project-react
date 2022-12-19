""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

apps.py -> настройки конфигурации приложения: about
"""
from django.apps import AppConfig


class AboutConfig(AppConfig):
    """Method required when the About application is created."""
    name = 'about'