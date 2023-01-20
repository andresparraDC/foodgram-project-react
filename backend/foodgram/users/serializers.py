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
from djoser.serializers import (
    UserSerializer, UserCreateSerializer, SetPasswordSerializer,
)
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD, settings.USER_ID_FIELD
                  ) + tuple(User.REQUIRED_FIELDS)
        read_only_fields = (settings.LOGIN_FIELD,)


class CustomUserCreateSerializer(UserCreateSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD,
                  settings.USER_ID_FIELD,
                  "password",
                  # 'is_subscribed',
                  ) + tuple(User.REQUIRED_FIELDS)

    # def get_is_subscribed(self, obj):
    #     request = self.context.get('request')
    #     if not request or request.user.is_anonymous:
    #         return False
    #     return Follow.objects.filter(
    #         user=obj.user, author=obj.author
    #     ).exists()


class CustomSetPasswordSerializer(SetPasswordSerializer):
    class Meta:
        fields = ('password',)
