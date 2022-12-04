from django.core.management.base import BaseCommand
# import csv
from reviews.models import Genre, Title
import pandas as pd

# to be modified
class Command(BaseCommand):
    help = 'import data Comment'

    def handle(self, *args, **options):
        df = pd.read_csv('static/data/genre_title.csv', sep=',')
        row_iter = df.iterrows()
        for index, row in row_iter:
            title = Title.objects.get(id=(row['title_id']))
            genre = Genre.objects.get(id=(row['genre_id']))
            title.genre.add(genre)
