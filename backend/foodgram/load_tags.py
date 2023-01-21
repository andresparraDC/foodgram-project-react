import csv
import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "foodgram.settings"
)
django.setup()


from foodgram_app.models import Tag


with open('tags.csv', encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Tag.objects.get_or_create(
            name=row[0],
            color=row[1],
            slug=row[2],
        )