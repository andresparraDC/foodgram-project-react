""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: admin.py
Описание файла: настройки панели администратора.
Классы:
 - UserAdmin
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
    )

    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)