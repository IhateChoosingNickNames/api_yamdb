import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

LIMIT: int = 30
SCORE_MIN = 0
SCORE_MAX = 10


class Category(models.Model):
    """Модель категорий."""

    pass


class Genre(models.Model):
    """Модель жанров."""

    pass


class Title(models.Model):
    """Модель произведений."""

    pass


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
            MinValueValidator(SCORE_MIN, "Допустимы значения от 0 до 10"),
            MaxValueValidator(SCORE_MAX, "Допустимы значения от 0 до 10"),
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
        ordering = ("author",)
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
        ordering = ("author",)
