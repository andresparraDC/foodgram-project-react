""" Спринт 14 Проект «Продуктовый помощник»  
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: apps.py
Описание файла: настройки конфигурации приложения: foodgram_app.
Классы:
 - FoodgramAppConfig
"""
from django.apps import AppConfig


class FoodgramAppConfig(AppConfig):
    """Метод, необходимый при создании приложения Foodgram."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodgram_app'