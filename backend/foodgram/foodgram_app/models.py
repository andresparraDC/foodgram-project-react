""" Спринт 14 Проект «Продуктовый помощник»
Автор   Фредди Андрес Парра
        Студент факультета Бэкенд. Когорта 14+

Имя файла: models.py
Описание файла: указание моделей, их взаимосвязи и
                указание таблиц для базы данных.
Классы:
 - Ingredient           класс, который генерирует модель: Ingredient.
 - Tag                  класс, который генерирует модель: Tag.
 - Recipe               класс, который генерирует модель: Recipe.
 - Favorite             класс, который генерирует модель: Favorite.
 - Follow               класс, который генерирует модель: Follow.
 - IngredientofRecipe   класс, который генерирует модель: IngredientofRecipe.
 - Purchase             класс, который генерирует модель: Purchase.

"""
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True
    )
    hex_regex = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6})$',
        message='Enter a valid hexfigure: e.g. "ff0022"'
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        validators=[hex_regex],
        unique=True
    )
    slug = models.SlugField(
        'Идентификатор tag',
        unique=True,
        max_length=200,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты, используемые в рецепте',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги, используемые для рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время должно быть больше 1 минуты'),),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Описание рецепта'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        validators=(
            MinValueValidator(
                1, message='Количество не может быть меньше 1'),),
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_recipe_ingredient',
            ),
        )
    
    def __str__(self):
        return 'Ингридиент в рецепте'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег рецепта'
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['tag', 'recipe'],
                                               name='unique_recipe_tag')]
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return 'Тег рецепта'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_user_favorite'
            )
        ]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shopping_cart'
        )]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
