""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: admin.py
Описание файла: настройки панели администратора.
Классы:
 - IngredientAdmin
 - IngredientofRecipeAdmin
 - RecipeAdmin
 - TagAdmin
 - PurchaseAdmin
 - FavoriteAdmin
 - SubscriptionAdmin
 - RecipeIngredientAdmin
"""
from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    #list_filter = ('name',)
    search_fields = (
        '^name',
    )
    empty_value_display = '-пусто-'


class IngredientInRecipeAdmin(admin.TabularInline):
    model = IngredientAmount
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author',
        'amount_favorites', 'amount_tags',
        'amount_ingredients',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    exclude = (
        'ingredients',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    inlines = [
        IngredientInRecipeAdmin,
    ]

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    def amount_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def amount_ingredients(obj):
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount',
    )
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
