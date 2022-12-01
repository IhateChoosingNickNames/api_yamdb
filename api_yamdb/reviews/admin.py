from django.contrib import admin

from reviews.models import Comment, Category, Review, Rating, Title, Genre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-пусто-"
    # list_editable = ("group",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-пусто-"
    # list_editable = ("group",)

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "description",  "category")
    search_fields = ("name",)
    empty_value_display = "-пусто-"

    # list_editable = ("group",)

# Заглушка
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "text", "pub_date", "score", "title")
    search_fields = ("author",)
    empty_value_display = "-пусто-"
    # list_editable = ("group",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "text", "pub_date", "title", "review")
    search_fields = ("author",)
    empty_value_display = "-пусто-"
    # list_editable = ("group",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "current_rating")
    search_fields = ("title",)
    empty_value_display = "-пусто-"
    # list_editable = ("group",)
