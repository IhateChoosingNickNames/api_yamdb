from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


User = get_user_model()

LIMIT: int = 30


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', max_length=50, unique=True)

    def __str__(self):
        """Строковое представление модели категорий."""
        return self.name[:LIMIT]

    class Meta:
        ordering = ("id", )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Слаг', max_length=50, unique=True)

    def __str__(self):
        """Строковое представление модели жанров."""
        return self.name[:LIMIT]

    class Meta:
        ordering = ("id", )
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        blank=False,
        validators=[MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name="title"
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name="title"
    )
    rating = models.ForeignKey(
        Rating,
        verbose_name='Рейтинг'
        on_delete=models.SET_DEFAULT,
        default=0,
        related_name="title"
    )

    def __str__(self):
        """Строковое представление модели произведений."""
        return self.name[:LIMIT]

    class Meta:
        ordering = ("id", )
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведение'

# Заглушки
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="review")
    class Meta:
        ordering = ("id", )


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="comment")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comment")
    class Meta:
        ordering = ("id", )


class Rating(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="rating")
    current_rating = models.IntegerField()
    class Meta:
        ordering = ("id", )
