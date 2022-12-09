from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import year_validator

User = get_user_model()

LIMIT: int = 30
SCORE_MIN: int = 1
SCORE_MAX: int = 10


class Category(models.Model):
    """Модель категорий."""
    name = models.TextField(
        verbose_name=_("Название категории"),
        max_length=256
    )
    slug = models.SlugField(
        verbose_name=_("Слаг для url"),
        max_length=50,
        unique=True
    )

    def __str___(self):
        return (self.name[:LIMIT])

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Genre(models.Model):
    """Модель жанров."""
    name = models.TextField(
        verbose_name=_("Название жанра"),
        max_length=256
    )
    slug = models.SlugField(
        verbose_name=_("Слаг для url"),
        max_length=50,
        unique=True
    )

    def __str___(self):
        return (self.name[:LIMIT])

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField(
        verbose_name=_('Название произведения'),
        max_length=256,
        blank=False
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_('Год выхода'),
        validators=[year_validator],
        blank=False
    )
    description = models.TextField(
        verbose_name=_('Описание произведения'),
        blank=True

    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True
    )

    def __str__(self):
        return self.name[:LIMIT]

    class Meta:
        verbose_name = _("Произведение")
        verbose_name_plural = _("Произведения")
        ordering = ("year",)


class Review(models.Model):
    """Модель отзывов."""

    author = models.ForeignKey(
        User, verbose_name=_("Автор отзыва"), on_delete=models.CASCADE
    )
    text = models.TextField(_("Текст отзыва"), max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.IntegerField(
        _("Оценка"),
        validators=[
            MinValueValidator(SCORE_MIN, "Допустимы значения от 1 до 10"),
            MaxValueValidator(SCORE_MAX, "Допустимы значения от 1 до 10"),
        ],
    )
    title = models.ForeignKey(
        Title,
        verbose_name=_("Произведение"),
        on_delete=models.CASCADE,
        related_name="review",
    )

    def __str__(self):
        return f"{self.author[:LIMIT]} - {self.text[:LIMIT]}"

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ("pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=("author", "title"), name="unique_review"
            ),
        )


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User, verbose_name=_("Автор комментария"), on_delete=models.CASCADE
    )
    text = models.CharField(_("Текст комментария"), max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        verbose_name=_("Отзыв"),
        on_delete=models.CASCADE,
        related_name="comment",
    )

    def __str__(self):
        return f"{self.author[:LIMIT]} - {self.text[:LIMIT]}"

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")
        ordering = ("pub_date",)
