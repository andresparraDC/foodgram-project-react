""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: views.py
Описание файла: опишите все контроллеры
Переменные:

"""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Recipe, Tag, User

from foodgram.settings import NUM_RECIPES_PAGE, NUM_RECIPESAUTHOR_PAGE


app_name = 'foodgram_app'


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
    recipes_list = Recipe.objects.all()
    paginator = Paginator(recipes_list, NUM_RECIPES_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Index Foodgram',
        'page_obj': page_obj,
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
    recipes = tag.recipes.all()[:NUM_RECIPES_PAGE]
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


def profile(request, username):
    author = User.objects.get(username=username)
    recipes = Recipe.objects.filter(author=author.pk)
    paginator = Paginator(recipes, NUM_RECIPESAUTHOR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    template = 'foodgram_app/profile.html'
    return render(
        request,
        template,
        context
    )


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'recipe': recipe,
    }
    template = 'foodgram_app/recipe_detail.html'
    return render(
        request,
        template,
        context
    )