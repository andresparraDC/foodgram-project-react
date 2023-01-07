from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Favorite, Follow, Ingredient, IngredientofRecipe, Recipe, Tag, User


class UserSerializer(serializers.ModelSerializer):
    """
    """
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        """
        """
        model = User
        fields = (
            'id', 'email',
            'username', 'first_name',
            'last_name', 'is_subscribed'
        )
     
    def get_is_subscribed(self, obj):
        """
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj.id
        ).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        """
        """
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        """
        """
        model = Tag
        fields = '__all__'


class IngredientofRecipeSerializer(serializers.ModelSerializer):
    """
    """
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
        """
        """
        model = IngredientofRecipe
        fields = (
            'id', 'name',
            'amount', 'measurement_unit'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """
    """
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientofRecipeSerializer(
        source='ingredients_amount'
        many=True,
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True
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
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
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
        recipe = Recipe.objects.create(
            image=image,
            **validated_data
        )
        self.get_ingredients_amount(ingredients, recipe)
        return recipe
    
    def update(self, instance, validated_data):
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        IngredientofRecipe.objects.filter(recipe=instance).delete()
        self.get_ingredients_amount(ingredients, instance)
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()
        return instance
