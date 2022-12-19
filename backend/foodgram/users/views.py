""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: views.py
Описание файла: 
Переменные:

"""
from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    """File to start the class: SignUp"""
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('foodgram_app:index')