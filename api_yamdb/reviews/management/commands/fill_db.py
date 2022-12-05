import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Title, Review, User


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    data_folder = "static/data"
    tables = (
        {"model": User, "file": "users.csv"},
        {"model": Genre, "file": "genre.csv"},
        {"model": Category, "file": "category.csv"},
        {"model": Title, "file": "titles.csv"},
        {"model": Title.genre.through, "file": "genre_title.csv"},
        {"model": Review, "file": "review.csv"},
        {"model": Comment, "file": "comments.csv"},
    )

    def handle(self, *args, **options):
        for table in self.tables:
            with open(
                os.path.join(self.data_folder, table["file"]), encoding="UTF-8"
            ) as file:
                rows = csv.DictReader(file)
                result = [table["model"](**row) for row in rows]
            table["model"].objects.bulk_create(result)
