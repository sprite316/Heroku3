import os
import urllib
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
from operator import itemgetter

django.setup()

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import json
import schedule
import time
import requests
from elections.models import Candidate
from hoobang.models import hoobang
from datetime import date, timedelta

Candidate.objects.all().delete()
hoobang.objects.all().delete()
