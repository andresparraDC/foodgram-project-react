""" Спринт 14 Проект «Продуктовый помощник»  
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: models.py
Описание файла: описывает класс даты создания.
Классы:
 - PubDateModel
"""
from django.db import models


class PubDateModel(models.Model):
    """Модель для определения даты создания."""
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        null=False,
        blank=False
    )

    class Meta:
        """Это абстрактная модель."""
        abstract = True 
