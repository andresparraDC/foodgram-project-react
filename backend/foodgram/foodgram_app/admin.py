""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

Имя файла: admin.py
Описание файла: настройки панели администратора.
Переменные:

"""
from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientofRecipe,
                     Purchase, Recipe, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class IngredientInRecipeAdmin(admin.TabularInline):
    model = IngredientofRecipe
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'favorited')
    list_filter = ('author', 'name', 'tags')
    exclude = ('ingredients',)

    inlines = [
        IngredientInRecipeAdmin,
    ]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = 'В избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, SubscriptionAdmin)
admin.site.register(IngredientofRecipe, RecipeIngredientAdmin)
