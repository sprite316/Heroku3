import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django

django.setup()

from HotList.models import HotList
from HoobangList.models import HoobangList

HotList.objects.all().delete()
HoobangList.objects.all().delete()
