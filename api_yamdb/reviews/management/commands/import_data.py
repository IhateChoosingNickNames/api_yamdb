from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
import pandas as pd


class Command(BaseCommand):
    help = 'import data Titel, Genre, Category'

    def handle(self, *args, **options):
        df = pd.read_csv('static/data/category.csv', sep=',')
        # print(df)
        row_iter = df.iterrows()
        objs = [
            Category(
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]

        Category.objects.bulk_create(objs)

        df = pd.read_csv('static/data/genre.csv', sep=',')
        # print(df)
        row_iter = df.iterrows()
        objs = [
            Genre(
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]

        Genre.objects.bulk_create(objs)

        df = pd.read_csv('static/data/titles.csv', sep=',')
        # print(df)
        row_iter = df.iterrows()
        objs = [
            Title(
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']),
            )
            for index, row in row_iter
        ]
        print(objs)
        Title.objects.bulk_create(objs)

        df = pd.read_csv('static/data/genre_title.csv', sep=',')
        row_iter = df.iterrows()
        for index, row in row_iter:
            title = Title.objects.get(id=(row['title_id']))
            genre = Genre.objects.get(id=(row['genre_id']))
            title.genre.add(genre)
