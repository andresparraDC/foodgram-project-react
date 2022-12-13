"""
Спринт 14
Проект: 
Автор: Фредди Андрес Парра

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
    path('', views.index),
    path('foodgram_app/', views.food_list),
    path('foodgram_app/<slug:slug>/', views.food_detail),
]
