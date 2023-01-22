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
#from weasyprint import HTML
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

from foodgram_app.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from .filters import IngredientNameFilter, RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
from django.template.loader import render_to_string


class TagsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с тегами.
    Добавить тег может администратор.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с ингредиентами.
    Добавить ингредиент может администратор.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    filter_backends = [IngredientNameFilter]
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """
    ViewSet для работы с рецептами.
    Для анонимов разрешен только просмотр рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__carts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        for i in ingredients:
            name = i[0]
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': i[1],
                    'amount': i[2],
                }
            else:
                shopping_list[name]['amount'] += i[2]
        wishlist = ([f'{item} - {value["amount"]} '
                     f'{value["measurement_unit"]} \n'
                     for item, value in shopping_list.items()])
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response
#        html_template = render_to_string('pdf_template.html',
#                                         {'ingredients': shopping_list})
#        html = HTML(string=html_template)
#        result = html.write_pdf()
#        response = HttpResponse(result, content_type='application/pdf;')
#        response['Content-Disposition'] = 'inline; filename=cart_list.pdf'
#        response['Content-Transfer-Encoding'] = 'binary'
#        return response
#        pdfmetrics.registerFont(
#            TTFont(
#                'Handicraft',
#                'Handicraft.ttf',
#                'UTF-8'
#            )
#        )
#        response = HttpResponse(
#            content_type='application/pdf'
#        )
#        response['Content-Disposition'] = ('attachment; '
#                                           'filename="shopping_list.pdf"')
#        page = canvas.Canvas(response)
#        page.setFont('Handicraft', size=24)
#        page.drawString(200, 800, 'Список покупок')
#        page.setFont('Handicraft', size=16)
#        for i, (name, data) in enumerate(shopping_list.items(), 1):
#            page.drawString(
#                75,
#                750,
#                (f'{i}. {name} - {data[2]} '
#                 f'{data[1]}')
#            )
#            height -= 25
#        page.showPage()
#        page.save()
#        return response
