import os
import sys
import pdb
import django

BASE_DIR = os.path.abspath('../mark-admin')

sys.path.append(BASE_DIR)

from markadmin import settings

INSTALLED_APPS = [
  'places.apps.PlacesConfig',
]

DATABASES = settings.DATABASES

SECRET_KEY = settings.SECRET_KEY

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "markparser.storage")

django.setup()

from places.models import Place

def get_places(q):
	places = Place.objects.filter(title__icontains=q)
	if places:
		return places[0]

def create_place(place):
	return Place(**place).save()
