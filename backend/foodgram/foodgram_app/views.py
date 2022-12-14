""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: views.py
Описание файла: опишите все контроллеры
Переменные:

"""
from django.shortcuts import get_object_or_404, render
from .models import Recipe, Tag


app_name = 'foodgram_app'
num_recipes = 6 # Esto se debe pasar a SETTINGS. "PENDIENTE"


def index(request):
    """
    Описание:     Главная страница
    Переменные:
    recipes       объекты модели рецепта
    context       словарь с информацией для отправки
                  в представление (HTML).
    --title       title of the "head" section of the website.
    --recipes     переменная с объектами (рецептами).
    template      HTML-файл, который вы используете в представлении.
    """
    recipes = Recipe.objects.all()[:num_recipes]
    context = {
        'title': 'Index Foodgram',
        'recipes': recipes,
    }
    template = 'foodgram_app/index.html'
    return render(
        request,
        template,
        context
    )


def tag_recipes(request, slug):
    """
    Описание:     
    Переменные:
    tag           ...
    recipes       ...
    context       словарь с информацией для отправки
                  в представление (HTML).
    --recipes     ...
    --tag         ...
    template      HTML-файл, который вы используете в представлении.
    """
    tag = get_object_or_404(Tag, slug=slug)
    recipes = tag.recipes.all()[:num_recipes]
    context = {
        'recipes': recipes,
        'tag': tag,
    }
    template = 'foodgram_app/tag_list.html'
    return render(
        request,
        template,
        context
    )