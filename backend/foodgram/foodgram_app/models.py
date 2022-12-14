""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: models.py
Описание файла: указание моделей, их взаимосвязи и
указание таблиц для базы данных.
Переменные:

"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Usuario(models.Model):
    email = models.EmailField(max_length=254)
    #username
    #first_name
    #last_name
    #password

class Ingredient(models.Model):
    """
    Описание:         Модел ингредиент.
    Переменные:
    name              Название ингредиентa.
    amount            Количество.
    measurement_unit  Единицы измерения.
    """
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )
    amount = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    measurement_unit = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    def __str__(self) -> str:
        """The title of Ingredient is displayed (string)""" 
        return f'{self.name}'


class Tag(models.Model):
    """
    Описание:     Модел тега.
    Переменные:
    name          Название тега.
    color         Цвет в HEX.
    slug          Уникальный слаг.
    """ 
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        primary_key=True,
        unique=True,
        max_length=200,
        blank=False
    )

    def __str__(self) -> str:
        """The title of Tag is displayed (string)""" 
        return f'{self.name}'


class Recipe(models.Model):
    """
    Описание:     Модел рецепты
    Переменные:
    author        Пользователь (В рецепте - автор рецепта)
    name          Название рецепта
    image         Ссылка на картинку на сайте
    text          Текстовое описание
    ingredients   Список ингредиентов
    tags          Список тегов
    cooking_time  Время приготовления (в минутах)
    """
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField(
        null=False,
        blank=False
    )
    image = models.TextField(
        null=False,
        blank=False
    )
    ingredients = models.ForeignKey(
        Ingredient,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tag = models.ForeignKey(
        Tag,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    #cooking_time
    pub_date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    class Meta:
        """Meta class of the Recipe model (by publication date).""" 
        ordering = ['-pub_date']
