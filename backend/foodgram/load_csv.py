import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodgram.settings")
django.setup()

import csv
from foodgram_app.models import Ingredient

with open('ingredients.csv', encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Ingredient.objects.get_or_create(
            name=row[0],
            measurement_unit=row[1],
        )
