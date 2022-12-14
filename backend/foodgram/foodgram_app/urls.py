""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: записывает все адреса в приложении: foodgram_app
Переменные:
 - urlpatterns: список адресов
   - 
"""
from django.urls import path

from . import views


app_name = 'foodgram_app'


urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:slug>/', views.tag_recipes, name="tag_list")
]
