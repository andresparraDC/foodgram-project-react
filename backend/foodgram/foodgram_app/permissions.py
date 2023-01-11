""" Спринт 14 Проект «Продуктовый помощник»  
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: permissions.py
Описание файла: разрешения пользователя.
Классы:
 - IsOwnerOrAdminOrReadOnly.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        if request.user and request.user.is_authenticated:
            return (
                request.user.is_superuser or request.user == obj.author
            )
        return False
