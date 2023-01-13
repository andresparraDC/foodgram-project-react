""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: models.py
Описание файла: указание моделей, их взаимосвязи и
                указание таблиц для базы данных (users).
Классы:
 - CustomUserManager
 - CustomUser
"""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    """
    def create_user(self, email,
                    username, first_name,
                    last_name, password):
        """
        """
        if not email:
            raise ValueError('Пользователи должны иметь имейль')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(
            using=self._db
        )
        return user

    def create_superuser(self, email,
                         username, first_name,
                         last_name, password):
        """
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(
            using=self._db
        )
        return user


class CustomUser(AbstractUser):
    """
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer.'
                  'Letters, digits and @/./+/-/_ only.',
        validators=[
            username_validator
        ],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(
        'First name',
        max_length=150
    )
    last_name = models.CharField(
        'Last name',
        max_length=150
    )
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
