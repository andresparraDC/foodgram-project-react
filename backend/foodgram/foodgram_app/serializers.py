from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Follow, Ingredient, IngredientofRecipe, Recipe, Tag, User


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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
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
        read_only=True
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


