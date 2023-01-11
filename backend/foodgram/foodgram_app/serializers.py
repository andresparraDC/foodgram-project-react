""" Спринт 14 Проект «Продуктовый помощник»  
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: serializers.py
Описание файла: сериализаторы проекта.
Классы:
 - IngredientSerializer.
 - TagSerializer.
 - IngredientofRecipeSerializer.
 - UserSerializer.
 - RecipeSerializer.
 - FollowerRecipeSerializer.
 - ShowFollowerSerializer.
 - FollowSerializer.
 - FavoriteSerializer.
 - PurchaseSerializer.
"""
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, Follow, Ingredient, IngredientofRecipe,
                     Purchase, Recipe, Tag, User)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientofRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода количества ингредиентов."""
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientofRecipe
        fields = (
            'id', 'name',
            'measurement_unit', 'amount'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed'
        )
    
    @transaction.atomic
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj.id
        ).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецепта."""
    image = Base64ImageField()
    author = UserSerializer(
        read_only=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientofRecipeSerializer(
        source='ingredients_amount',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags',
            'author', 'name',
            'text', 'image',
            'ingredients', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Purchase.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_ingredients_amount(self, ingredients, recipe):
        tags = self.initial_data.get('tags')
        for tag_id in tags:
            recipe.tags.add(
                get_object_or_404(
                    Tag,
                    pk=tag_id
                )
            )
        for ingredient in ingredients:
            ingredients_amount = IngredientofRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredients_amount.save()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        # проверка ингредиентов.
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    {
                        'amount': 'Убедитесь, что значение количества '
                                  'ингредиента больше нуля.'
                    }
                )
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredients_set:
                raise serializers.ValidationError(
                    {
                        'ingredients': 'Ингредиент в рецепте не должен повторяться.'
                    }
                )
            ingredients_set.add(ingredient_id)
        data['ingredients'] = ingredients
        # проверка тегов.
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {
                    'tags': 'Необходимо добавить хотя бы один тэг.'
                }
            )
        # проверка времени приготовления.
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                {
                    'cooking_time': 'Время приготовления должно быть больше нуля.'
                }
            )
        # возврат подтвержденных данных. (return of data validated).
        return data

    @transaction.atomic
    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            image=image,
            **validated_data
        )
        self.get_ingredients_amount(
            ingredients,
            recipe
        )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientofRecipe.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        self.get_ingredients_amount(ingredients, instance)
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        return super().update(instance, validated_data)


class FollowerRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецепта последователя."""
    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )


class ShowFollowerSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения последователя."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email',
            'username', 'first_name',
            'last_name','is_subscribed',
            'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit is not None:
            queryset = Recipe.objects.filter(
                author=obj.author
            )[:int(limit)]
        return FollowerRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(
            author=obj.author
        ).count()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для последующего."""
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        request = self.context.get('request')
        author_id = data['author'].id
        if request.user.id == author_id:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя.'
            )
        if Follow.objects.filter(
                user=request.user,
                author__id=author_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return data


class FavoritesSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        favorite_exists = Favorite.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()
        if favorite_exists:
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowerRecipeSerializer(
            instance.recipe,
            context=context).data


class PurchaseSerializer(FavoritesSerializer):
    """Сериализатор для покупки."""
    class Meta(FavoritesSerializer.Meta):
        model = Purchase

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = Purchase.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()
        if purchase_exists:
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowerRecipeSerializer(
            instance.recipe,
            context=context).data
