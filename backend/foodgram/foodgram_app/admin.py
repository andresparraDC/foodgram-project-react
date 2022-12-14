""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

Имя файла: admin.py
Описание файла: настройки панели администратора.
Переменные:

"""
from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Handling the Recipe model data from the administrator."""
    list_display = (
        'name',
        'author',
        'text',
        'image',
        'pub_date',
    )
    search_fields = ('text',) 
    list_filter = ('author','pub_date',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Handling the Tag model data from the administrator."""
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',) 
    list_filter = ('color',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """Handling the Ingredient model data from the administrator."""
    list_display = (
        'name',
        'amount',
        'measurement_unit',
    )
    search_fields = ('name',) 
    list_filter = ('amount',)
    empty_value_display = '-пусто-' 


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)