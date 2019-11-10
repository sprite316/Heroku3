from django.shortcuts import render
from django.http import HttpResponse
from .models import Candidate
import json
from django.core.paginator import Paginator
'''
def index(request):
    candidates = Candidate.objects.all()
    context = {'candidates':candidates}
    return render(request, 'elections/index.html', context)
'''

def index(request):
    candidates = Candidate.objects.all()

    candidate_list = Candidate.objects.all()
    paginator = Paginator(candidate_list, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'elections/index.html', {
    'candidates':candidates, 'posts':posts
    })
