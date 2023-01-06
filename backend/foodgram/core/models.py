from django.db import models


class PubDateModel(models.Model):
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        null=False,
        blank=False
    )

    class Meta:
        # Это абстрактная модель:
        abstract = True 
