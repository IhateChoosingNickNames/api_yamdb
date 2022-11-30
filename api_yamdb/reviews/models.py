from django.contrib.auth import get_user_model  # to be deleted
from django.db import models
from django.core.validators import MaxValueValidator
import datetime

User = get_user_model()  # to be deleted

LIMIT: int = 30


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        """Строковое представление модели категорий."""
        return self.name[:LIMIT]


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        """Строковое представление модели жанров."""
        return self.name[:LIMIT]


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        blank=False,
        validators=[MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )
    raiting = models.IntegerField(null=True, default=None)  # средний на основании оценок, которые ставят пользователи

    def __str__(self):
        """Строковое представление модели произведений."""
        return self.name[:LIMIT]
