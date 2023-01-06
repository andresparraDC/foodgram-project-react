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


class FavoriteAdmin(admin.ModelAdmin):
    """Handling the Favorite model data from the administrator."""
    list_display = (
        'user',
        'recipe'
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'author', 
        'user'
    )


class IngredientAdmin(admin.ModelAdmin):
    """Handling the Ingredient model data from the administrator."""
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('^name',)
    empty_value_display = '-пусто-'


class IngredientofRecipeAdmin(admin.TabularInline):
    model = IngredientofRecipe
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    """Handling the Recipe model data from the administrator."""
    list_display = (
        'author',
        'name',
        'favorited'
    ) 
    list_filter = (
        'author',
        'name',
        'tags'
    )
    exclude = (
        'ingredients',
    )
    inlines = [
        IngredientofRecipeAdmin,
    ]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count
    
    favorited.short_description = 'В избранном'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


class TagAdmin(admin.ModelAdmin):
    """Handling the Tag model data from the administrator."""
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
    ) 
    list_filter = (
        'color',
    )
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientofRecipe, IngredientofRecipeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
