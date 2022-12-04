import pandas as pd

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    """Команда для загрузки данных из CSV"""

    help = 'import data for Title, Genre, Category, Review, Comment, User'

    def handle(self, *args, **options):
        df = pd.read_csv('static/data/category.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Category(
                pk=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]

        Category.objects.bulk_create(objs)

        df = pd.read_csv('static/data/genre.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Genre(
                pk=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]

        Genre.objects.bulk_create(objs)

        df = pd.read_csv('static/data/titles.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Title(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']),
            )
            for index, row in row_iter
        ]

        Title.objects.bulk_create(objs)

        df = pd.read_csv('static/data/genre_title.csv', sep=',')
        row_iter = df.iterrows()

        for index, row in row_iter:
            title = Title.objects.get(id=(row['title_id']))
            genre = Genre.objects.get(id=(row['genre_id']))
            title.genre.add(genre)

        df = pd.read_csv('static/data/users.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            User(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=['first_name'],
                last_name=['last_name']
            )
            for index, row in row_iter
        ]

        User.objects.bulk_create(objs)

        df = pd.read_csv('static/data/review.csv', sep=',')
        row_iter = df.iterrows()
        objs_review = [
            Review(
                pk=row['id'],
                author=User.objects.get(id=row['author']),
                text=row['text'],
                pub_date=row['pub_date'],
                score=row['score'],
                title_id=row['title_id'],
            )
            for index, row in row_iter
        ]

        Review.objects.bulk_create(objs_review)

        df = pd.read_csv('static/data/comments.csv', sep=',')
        row_iter = df.iterrows()
        objs = [
            Comment(
                pk=row['id'],
                author=User.objects.get(id=row['author']),
                text=row['text'],
                pub_date=row['pub_date'],
                review=Review.objects.get(id=row['review_id']),
            )
            for index, row in row_iter
        ]

        Comment.objects.bulk_create(objs)
