""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

Имя файла: admin.py
Описание файла: настройки панели администратора.
Переменные:
    IngredientAdmin
    IngredientofRecipeAdmin
    RecipeAdmin
    TagAdmin
    PurchaseAdmin
    FavoriteAdmin
    SubscriptionAdmin
    RecipeIngredientAdmin
"""
from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientofRecipe,
                     Purchase, Recipe, Tag)


class FavoriteAdmin(admin.ModelAdmin):
    """модель Favorite включена в панели администратора."""
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    """модель Subscription включена в панели администратора."""
    list_display = ('author', 'user')


class IngredientAdmin(admin.ModelAdmin):
    """модель Ingredient включена в панели администратора."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    """модель RecipeIngredient включена в панели администратора."""
    list_display = ('recipe', 'ingredient', 'amount')


class IngredientofRecipeAdmin(admin.TabularInline):
    """модель IngredientofRecipe включена в панели администратора."""
    model = IngredientofRecipe
    fk_name = 'recipe'


class PurchaseAdmin(admin.ModelAdmin):
    """модель Purchase включена в панели администратора."""
    list_display = ('user', 'recipe')


class RecipeAdmin(admin.ModelAdmin):
    """модель Recipe включена в панели администратора."""
    list_display = ('author', 'name', 'favorited')
    list_filter = ('author', 'name', 'tags')
    exclude = ('ingredients',)

    inlines = [
        IngredientofRecipeAdmin,
    ]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(
            recipe=obj
        ).count()
        return favorited_count

    favorited.short_description = 'В избранном'


class TagAdmin(admin.ModelAdmin):
    """модель Tag включена в панели администратора."""
    list_display = ('name', 'color', 'slug')


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientofRecipe, RecipeIngredientAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
