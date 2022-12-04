from django.core.management.base import BaseCommand
from users.models import User
import pandas as pd


class Command(BaseCommand):
    help = 'import Users'

    def handle(self, *args, **options):
        df = pd.read_csv('static/data/users.csv', sep=',')
        print(df)
        row_iter = df.iterrows()
        objs = [
            User(
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
