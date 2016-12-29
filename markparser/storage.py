import os
import sys
import pdb
sys.path.append(os.path.abspath('../mark-admin'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
if False:
  import django
  django.setup()

  from places.models import Place
  from django.db.models import Q

  def get_places(q):
    places = Place.objects.filter(Q(title_ru__icontains=q) | Q(title_ua__icontains=q))
    if places:
      return places[0]

  def create_place(place):
    return Place(**place).save()
