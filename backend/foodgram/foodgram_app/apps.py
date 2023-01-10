""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

apps.py -> настройки конфигурации приложения: foodgram_app
"""
from django.apps import AppConfig


class FoodgramAppConfig(AppConfig):
    """Method required when the Foodgram application is created."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodgram_app'