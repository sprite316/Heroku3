from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader
from .models import hoobang
import json
from django.core.paginator import Paginator

# list of mobile User Agents
mobile_uas = [
    'w3c ', 'acs-', 'alav', 'alca', 'amoi', 'audi', 'avan', 'benq', 'bird', 'blac',
    'blaz', 'brew', 'cell', 'cldc', 'cmd-', 'dang', 'doco', 'eric', 'hipt', 'inno',
    'ipaq', 'java', 'jigs', 'kddi', 'keji', 'leno', 'lg-c', 'lg-d', 'lg-g', 'lge-',
    'maui', 'maxo', 'midp', 'mits', 'mmef', 'mobi', 'mot-', 'moto', 'mwbp', 'nec-',
    'newt', 'noki', 'oper', 'palm', 'pana', 'pant', 'phil', 'play', 'port', 'prox',
    'qwap', 'sage', 'sams', 'sany', 'sch-', 'sec-', 'send', 'seri', 'sgh-', 'shar',
    'sie-', 'siem', 'smal', 'smar', 'sony', 'sph-', 'symb', 't-mo', 'teli', 'tim-',
    'tosh', 'tsm-', 'upg1', 'upsi', 'vk-v', 'voda', 'wap-', 'wapa', 'wapi', 'wapp',
    'wapr', 'webc', 'winw', 'winw', 'xda', 'xda-'
]
mobile_ua_hints = ['SymbianOS', 'Opera Mini', 'iPhone']


def index(request):
    hoobangs = hoobang.objects.all()
    hoobang_list = hoobang.objects.all()
    paginator = Paginator(hoobang_list, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # [2]
    page_numbers_range = 6

    # [3]
    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    # [4]
    if end_index >= max_index:
        end_index = max_index
    paginator_range = paginator.page_range[start_index:end_index]

    return render(request, 'hoobang/index.html', {
        'hoobangs': hoobangs, 'posts': posts, 'paginator_range': paginator_range
    })


'''
def index(request):
    candidates = Candidate.objects.all().order_by('-count')[0:10]
    #candidate_list = Candidate.objects.all()
    #paginator = Paginator(candidate_list, 20)
    #page = request.GET.get('page')


    if mobileBrowser(request):
        return render(request, 'elections/m_index.html', {
        'candidates':candidates
        })
    else:
        return render(request, 'elections/index.html', {
        'candidates':candidates
        })
'''
