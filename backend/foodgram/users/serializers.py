""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: serializers.py
Описание файла: сериализаторы проекта (users).
Классы:
 - CustomUserSerializer
 - CustomUserCreateSerializer
 - CustomSetPasswordSerializer
"""
from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import (SetPasswordSerializer, UserCreateSerializer,
                                UserSerializer)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор CustomUser"""
    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD
        ) + tuple(
            User.REQUIRED_FIELDS
        )
        read_only_fields = (
            settings.LOGIN_FIELD,
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор CustomUserCreate"""
    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
        ) + tuple(
            User.REQUIRED_FIELDS
        )


class CustomSetPasswordSerializer(SetPasswordSerializer):
    """Сериализатор CustomSetPassword"""
    class Meta:
        fields = (
            'password',
        )
