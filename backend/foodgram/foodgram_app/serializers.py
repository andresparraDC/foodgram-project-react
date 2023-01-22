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

# LISTO
class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов
    """
    class Meta:
        model = Tag
        fields = '__all__'
        #read_only_fields = '__all__',

# LISTO
class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов
    """
    class Meta:
        model = Ingredient
        fields = '__all__'
        #read_only_fields = '__all__',

# LISTO
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


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount',)

# LISTO
class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов
    """
#    author = CustomUserSerializer(
#        read_only=True
#    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

#    tags = TagSerializer(
#        many=True,
#        read_only=True
#    )

    ingredients = IngredientAmountSerializer(
        source='ingredients_recipe',
        many=True,
        read_only=True
    )

    image = Base64ImageField()

    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )

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
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()

# LISTO
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

# LISTO
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

    def get_ingredients_amount(self, tags, ingredients, recipe):
        #tags = self.initial_data.get('tags')
        for tag_id in tags:
            recipe.tags.add(
                get_object_or_404(
                    Tag,
                    pk=tag_id
                )
            )
        for ingredient in ingredients:
            ingredients_amount = IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            ingredients_amount.save()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Количество ингредиента должно быть больше нуля!'
                })
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
        tags_list = []
        for tag_item in tags:
            tag = get_object_or_404(Tag, id=tag_item)
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Теги в рецепте не должны повторяться'}
                )
            tags_list.append(tag)
        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть больше 0!'
            })
        data['author'] = self.context.get('request').user
        data['ingredients'] = ingredients
        data['cooking_time'] = cooking_time
        data['tags'] = tags
        return data

    def create_ingredients(self, ingredients, recipe):
        """Создаем связку ингредиентов для рецепта"""
        for ingredient_item in ingredients:
            IngredientAmount.objects.bulk_create(
                [IngredientAmount(
                    ingredient_id=ingredient_item['id'],
                    recipe=recipe,
                    amount=ingredient_item['amount']
                )]
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(
            author=author,
            image=image,
            **validated_data
        )
        recipe.tags.set(tags)
        #self.get_ingredients_amount(tags, ingredients, recipe)
        self.create_ingredients(ingredients, recipe)
        recipe.save()
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.get_ingredients_amount(tags=tags, ingredients=ingredients, recipe=instance)
        return super().update(instance, validated_data)

# LISTO
class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения сведений о рецепте
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

# LISTO
class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка избранного
    """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(
            user=request.user,
            recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже есть в избранном!'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data

# LISTO
class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка покупок
    """
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

#    def validate(self, data):
#        request = self.context.get('request')
#        recipe_id = data['recipe'].id
#        purchase_exists = ShoppingCart.objects.filter(
#            user=request.user,
#            recipe__id=recipe_id
#        ).exists()
#        if purchase_exists:
#            raise serializers.ValidationError(
#                'Рецепт уже в списке покупок'
#            )
#        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe,
            context=context
        ).data
