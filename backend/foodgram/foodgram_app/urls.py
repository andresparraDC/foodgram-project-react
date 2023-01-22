""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: записывает все адреса в приложении: foodgram_app
Переменные:
 - urlpatterns: список адресов
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from users.views import CustomUserViewSet


app_name = 'foodgram_app'


router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
