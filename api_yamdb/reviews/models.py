from django.db import models
from django.core.validators import MaxValueValidator
import datetime


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        """Строковое представление модели категорий."""
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        """Строковое представление модели жанров."""
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        blank=False,
        validators=[MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        through="GenresForTitle",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        """Строковое представление модели произведений."""
        return self.name


class GenresForTitle(models.Model):
    """Модель для связи проиведений и жанров."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
