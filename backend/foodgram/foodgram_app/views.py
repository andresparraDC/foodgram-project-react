"""
Спринт 14
Проект: 
Автор: Фредди Андрес Парра

Имя файла: views.py
Описание файла: опишите все контроллеры
Переменные:

"""
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    template = 'foodgram_app/index.html'
    context = {
        'title': 'Index Foodgram'
    }
    return render(
        request,
        template,
        context
    )

def food_list(request):
    template = 'foodgram_app/list.html'
    context = {
        'title': 'List Foodgram'
    }
    return render(
        request,
        template,
        context
    )

def food_detail(request, slug):
    template = 'foodgram_app/detail.html'
    context = {
        'slug': slug,
        'title': f'Details of Food: {slug}',
    }
    return render(
        request,
        template,
        context
    )