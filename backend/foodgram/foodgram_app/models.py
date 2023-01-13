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
from core.models import PubDateModel
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """
    Описание: Модел ингредиент.
    Переменные:
     - name              Название ингредиентa.
     - amount            Количество.
     - measurement_unit  Единицы измерения.
    """
    name = models.CharField(
        'Название',
        max_length=200,
        null=False,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name', 'measurement_unit'
                ],
                name='unique ingredient'
            )
        ]

    def __str__(self) -> str:
        """Отображается название и единица измерения ингредиента (строка).""" 
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Описание: Модел тега.
    Переменные:
     - name     Название тега.
     - color    Цвет в HEX.
     - slug     Уникальный слаг.
    """ 
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True,
        blank=False,
        db_index=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f0-9]{6})$',
                message='Введите действительный hexfigure: например: "fc2321"'
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name='тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        """Отображается название тега (строка).""" 
        return f'Название тега: {self.name}'


class Recipe(PubDateModel):
    """
    Описание: Модел рецепты
    Переменные:
     - author        Пользователь (В рецепте - автор рецепта).
     - name          Название рецепта.
     - image         Ссылка на картинку на сайте.
     - text          Текстовое описание.
     - ingredients   Список ингредиентов.
     - tags          Список тегов.
     - cooking_time  Время приготовления (в минутах).
     - created      переменная: created из модели PubDateModel (приложение: core).
    """
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField(
        'Описание рецепта',
        null=False,
        blank=False
    )
    image = models.ImageField(
        'Изображение',
        null=False,
        blank=False,
        upload_to='recipes/'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        blank=False,
        through='IngredientofRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=False,
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Время должно быть больше 1 минуты.'
            )
        ]
    )

    class Meta: 
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created']

    def __str__(self) -> str:
        """Отображается название рецепта (строка)."""
        return f'{self.name}'


class Favorite(PubDateModel):
    """
    Описание: Модель Любимый рецепт.
    Переменные:
     - user         пользователь, которому нравится рецепт.
     - recipe       любимый рецепт.
     - created      переменная: created из модели PubDateModel (приложение: core).
    """    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite_subscriber',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = 'Избранное',
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user', 'recipe'
                ],
                name='favorite_user_recept_unique'
            )
        ]
    
    def __str__(self) -> str:
        """Отображается любимый рецепт пользователя (строка)."""
        return f'Рецепт {self.recipe} в избранном пользователя {self.user}'


class Follow(PubDateModel):
    """
    Описание: Модель для подписчиков.
    Переменные:
     - user     follower.
     - author   following.
     - created  переменная: created из модели PubDateModel (приложение: core).
    """  
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='follow_unique'
            )
        ]
    
    def __str__(self) -> str:
        """Это показывает, что пользователь подписался на автора (строка)."""
        return f'{self.user} подписан на {self.author}'


class IngredientofRecipe(models.Model):
    """
    Описание: Модел ингредиенты рецепта
    Переменные:
     - amount        Количество ингредиента.
     - ingredient    используемый ингредиент.
     - recipe        приготовленный рецепт.
    """
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
         validators=[
            MinValueValidator(
                1,
                message='Количество не может быть меньше 1.'
            )
        ]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredients_amount',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients_amount',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Количество ингредиента',
        verbose_name_plural = 'Количество ингредиентов',
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'ingredient', 'recipe'
                ],
                name='recipe_ingredient_unique',
            )
        ]


class Purchase(PubDateModel):
    """
    Описание: Модель Purchase.
    Переменные:
     - user      пользователь, который будет покупать.
     - recipe    рецепт для покупки.
     - created   переменная: created из модели PubDateModel (приложение: core).       
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-created'],
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='purchase_user_recipe_unique'
            )
        ]
    
    def __str__(self) -> str:
        """Покажите, что рецепт есть в списке покупок пользователя."""
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
