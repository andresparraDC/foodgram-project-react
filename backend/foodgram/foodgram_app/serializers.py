""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: serializers.py
Описание файла: сериализаторы проекта (foodgram_app).
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
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foodgram_app.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag, User)
from users.serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404

class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов
    """
    class Meta:
        model = Tag
        fields = '__all__'
        #read_only_fields = '__all__',


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов
    """
    class Meta:
        model = Ingredient
        fields = '__all__'
        #read_only_fields = '__all__',


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода количества ингредиентов
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        queryset = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления Ингредиентов
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = (
            'id', 'name',
            'amount', 'measurement_unit'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления рецептов
    """
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = AddIngredientSerializer(
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
            'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_ingredients_amount(self, ingredients, recipe):
        tags = self.initial_data.get('tags')
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))
        for ingredient in ingredients:
            ingredients_amount = IngredientAmount.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredients_amount.save()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Убедитесь, что значение количества '
                     'ингредиента больше нуля')
                )
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(ingredient_id)
        data['ingredients'] = ingredients
        if int(self.initial_data.get('cooking_time')) <= 0:
            raise serializers.ValidationError(
                ('Время приготовления должно быть '
                 'больше нуля')
            )
        tags = self.initial_data.get('tags')
        if tags is None:
            raise serializers.ValidationError(
                ('Необходимо добавить хотя бы'
                 'один тэг')
            )
        return data

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(
            image=image,
            author=author,
            **validated_data
        )
        self.get_ingredients_amount(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.get_ingredients_amount(ingredients, instance)
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()
        return super().update(instance, validated_data)


class FollowerRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения сведений о рецепте
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка избранного
    """
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe_id = data['recipe'].id
        favorite_exists = Favorite.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()
        if favorite_exists:
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowerRecipeSerializer(
            instance.recipe, context=context).data


class ShoppingCartSerializer(FavoriteSerializer):
    """
    Сериализатор для списка покупок
    """
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = ShoppingCart.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()
        if purchase_exists:
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowerRecipeSerializer(
            instance.recipe,
            context=context
        ).data
