""" Спринт 14 Проект «Продуктовый помощник»
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: views.py
Описание файла: опишите все контроллеры
Классы:
 - CustomUserViewSet
 - TagViewSet
 - IngredientsViewSet
 - RecipeViewSet
"""
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.db.models import Sum
from .models import (Favorite, Ingredient, RecipeIngredient, Recipe,
                            ShoppingList, Tag)

from .pagination import CustomPageNumberPagination
from .serializers import IngredientsSerializer, TagsSerializer, ShowRecipeFullSerializer
from .serializers import AddRecipeSerializer, FavouriteSerializer, ShoppingListSerializer
from django.template.loader import render_to_string
from rest_framework import permissions, status, viewsets
from .mixins import RetriveAndListViewSet
from .filters import IngredientsFilter, RecipeFilter
from .permissions import IsAuthorOrAdmin
from .utils import download_file_response


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = ShowRecipeFullSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="favorite",
        permission_classes=[IsAuthorOrAdmin],
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"error": "Этот рецепт уже в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavouriteSerializer(favorite,
                                             context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="shopping_cart",
        permission_classes=[IsAuthorOrAdmin],
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"error": "Этот рецепт уже в корзине покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shoping_cart = ShoppingList.objects.create(user=user,
                                                       recipe=recipe)
            serializer = ShoppingListSerializer(
                shoping_cart, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            delete_shoping_cart = ShoppingList.objects.filter(user=user,
                                                              recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        return download_file_response(ingredients_list)
