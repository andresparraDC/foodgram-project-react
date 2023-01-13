""" Спринт 14 Проект «Продуктовый помощник»
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: user_filters.py
Описание файла:
Переменные:
"""
from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(
        attrs={
            'class': css
        }
    )
