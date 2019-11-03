from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

import json
# Create your views here.

def index(request):
    #Candidate.objects.all().delete()
    candidates = Candidate.objects.all()
    context = {'candidates':candidates}
    return render(request, 'elections/index.html', context)

'''
def index(request):
    Candidate.objects.all().delete()
    candidates = Candidate.objects.all()

    with open('./elections/title_link.json', 'rt', encoding='utf-8-sig') as json_file:
        json_data = json.load(json_file)

    for i in range(len(json_data)):
    #for i in range(5):
        new_candidate = Candidate(date=json_data[i]["day"],
        title=json_data[i]["title"],
        count=json_data[i]["count"],
        link=json_data[i]["link"])
        new_candidate.save()

    context = {'candidates':candidates}
    return render(request, 'elections/index.html', context)
'''
