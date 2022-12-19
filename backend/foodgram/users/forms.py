""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: forms.py
Описание файла: 
Переменные:

"""
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    """Form of user creation"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')