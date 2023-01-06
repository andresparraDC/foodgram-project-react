""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: paginator.py
Описание файла: Запустите Paginator из Django.
Переменные:
"""
from django.core.paginator import Paginator

from foodgram.settings import NUM_RECIPES_PAGE, NUM_RECIPESAUTHOR_PAGE


def paginator_recipes(request, recipes, var):
    """
    """
    paginator = Paginator(recipes, NUM_RECIPES_PAGE)
    if var == 2:
        paginator = Paginator(recipes, NUM_RECIPESAUTHOR_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
