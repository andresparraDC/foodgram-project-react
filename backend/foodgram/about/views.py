""" Спринт 14 Проект «Продуктовый помощник»  
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: views.py
Описание файла: опишите все контроллеры
Классы:
 - AboutAuthorView
 - AboutTechView
"""
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Чтобы загрузить статическую страницу с
    описанием информации об авторе."""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Чтобы загрузить статическую страницу,
    описывающую использованную технологию."""
    template_name = 'about/tech.html'
