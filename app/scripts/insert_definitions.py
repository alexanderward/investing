import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investing.settings")
import django
django.setup()
from app.models import Definition

definitions = json.load(file('definitions/initial.json'))
Definition.objects.all().delete()
definitions = [x.get('fields') for x in definitions]
for definition in definitions:
    Definition.objects.create(title=definition.get('title'), definition=definition.get('definition'), category='General')

