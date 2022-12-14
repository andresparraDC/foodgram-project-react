""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

apps.py -> настройки конфигурации приложения
"""
from django.apps import AppConfig


class FoodgramAppConfig(AppConfig):
    """Method required when the Foodgram application is created."""
    name = 'foodgram_app'
