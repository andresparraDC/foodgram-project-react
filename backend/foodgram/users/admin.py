""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: admin.py
Описание файла: настройки панели администратора.
Классы:
 - UserAdmin
"""
from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email',
        'first_name', 'last_name'
    )

    fields = (
        'first_name', 'last_name',
        'username', 'email',
    )
    #search_fields = ('username', 'email')
    #list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'author'
    )
    search_fields = (
        'user', 'author'
    )
    list_filter = (
        'user', 'author'
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Follow, FollowAdmin)