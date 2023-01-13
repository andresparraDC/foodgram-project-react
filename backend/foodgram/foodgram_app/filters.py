""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: filters.py
Описание файла: фильтры для модели Ingredient и Recipe.
Классы:
 - IngredientNameFilter
 - RecipeFilter
"""
import django_filters as filters

from .models import Ingredient, Recipe, User


class IngredientNameFilter(filters.FilterSet):
    """Фильтр по названию ингредиента. (istartswith)"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        """Отобразите 2 поля модели ингредиентов."""
        model = Ingredient
        fields = ('name', 'measurement_unit')


class RecipeFilter(filters.FilterSet):
    """Отфильтруйте рецепты по тегам, автору, в избранном
    или в корзине покупок.
    """
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        """Отобразите 4 поля модели рецепта."""
        model = Recipe
        fields = [
            'tags', 'author',
            'is_favorited', 'is_in_shopping_cart'
        ]

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(
                favorite_recipe__user=user
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(
                purchases__user=user
            )
        return queryset
