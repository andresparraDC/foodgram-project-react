""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: views.py
Описание файла: опишите все контроллеры
Переменные:

"""
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    '''To load the static page describing 
    the author information.'''
    template_name = 'about/author.html'

class AboutTechView(TemplateView):
    '''To load the static page describing the 
    technology that was used.'''
    template_name = 'about/tech.html'
