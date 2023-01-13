""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: load_csv.py
Описание файла: импортируйте CSV-файл ингредиентов.
"""
import csv
import os
import django

from foodgram_app.models import Ingredient


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "foodgram.settings"
)
django.setup()


with open('ingredients.csv', encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Ingredient.objects.get_or_create(
            name=row[0],
            measurement_unit=row[1],
        )
