""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: записывает все адреса в приложении: about
Переменные:
 - urlpatterns: список адресов
"""
from django.urls import path

from . import views


app_name = 'about'


urlpatterns = [ 
    # 
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    #  
    path('tech/', views.AboutTechView.as_view(), name='tech'), 
] 