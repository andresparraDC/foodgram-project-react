""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+ 

filters.py -> 
"""
import django_filters as filters

from .models import Ingredient, User, Recipe


class IngredientNameFilter(filters.FilterSet):
    """
    """
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswitch'
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
            'measurement_unit'
        )

class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags_slug'
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
        model = Recipe
        fields = [
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        ]
    
    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(Favorite_recipe__user=user)
        return queryset
    
    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(purchase__user=user)
        return queryset
