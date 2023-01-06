""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: models.py
Описание файла: указание моделей, их взаимосвязи и
указание таблиц для базы данных.
Переменные:
    Favorite                Description of Favorite
    Follow                  Description of Follow
    Ingredient              Description of Ingredient
    IngredientofRecipe      Description of IngredientofRecipe
    Purchase                Description of Purchase
    Recipe                  Description of Recipe
    Tag                     Desciption for Tag
"""
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model

from core.models import PubDateModel

User = get_user_model()


class Ingredient(models.Model):
    """
    Описание:         Модел ингредиент.
    Переменные:
    name              Название ингредиентa.
    amount            Количество.
    measurement_unit  Единицы измерения.
    """
    name = models.CharField(
        'Название',
        max_length=200,
        null=False,
        blank=False
    )
    ##
    ##amount = models.CharField(
    ##    max_length=50,
    ##    null=False,
    ##    blank=False
    ##)
    ##
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

    def __str__(self) -> str:
        """The name and unit of measurement of Ingredient is displayed (string)""" 
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Описание:     Модел тега.
    Переменные:
    name          Название тега.
    color         Цвет в HEX.
    slug          Уникальный слаг.
    """ 
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
        blank=False,
        db_index=True
    )
    color = models.CharField(
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
        """
        """
        verbose_name='тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        """The name of Tag is displayed (string)""" 
        return f'Название тега: {self.name}'


class Recipe(PubDateModel):
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
        'Название',
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
        'Описание',
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
        verbose_name='Ингредиент',
        blank=False,
        # foodgram_app.Recipe.ingredients: (fields.W340)
        # null has no effect on ManyToManyField.
        # null=False,
        through='IngredientofRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=False,
        # foodgram_app.Recipe.ingredients: (fields.W340)
        # null has no effect on ManyToManyField.
        # null=False,
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Не менее 1.'
            )
        ]
    )

    class Meta:
        """Meta class of the Recipe model (by publication date).""" 
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        """The name of Recipe is displayed (string)"""
        return f'{self.name}'


class IngredientofRecipe(models.Model):
    """
    Описание:     Модел ингредиенты рецепта
    Переменные:
    amount        
    ingredient    
    recipe        
    """
    amount = models.PositiveIntegerField(
        'Количество ингредиента',
        #max_length=50,
        #null=False,
        #blank=False
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredients_amount',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients_amount',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Количество ингредиента',
        verbose_name_plural = 'Количество ингредиентов',
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient_unique'
            )
        ]


class Favorite(PubDateModel):
    """
    Описание:     Модель Любимый рецепт.
    Переменные:
    user  
    recipe    
    date_added        
    """    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_subscriber'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранное',
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_user_recept_unique'
            )
        ]
    
    def __str__(self) -> str:
        """The recipe of user is displayed (string)"""
        return f'Рецепт {self.recipe} в избранном пользователя {self.user}'


class Follow(PubDateModel):
    """
    Описание:     Модель для подписчиков.
    Переменные:
    user  
    author    
    following_date        
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
        """It shows that the user subscribed to the author"""
        return f'{self.user} подписан на {self.author}'


class Purchase(PubDateModel):
    """
    Описание:     Модель Purchase.
    Переменные:
    user  
    recipe    
    date_purching        
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
        """Display that the recipe is on the shopping list of user."""
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
