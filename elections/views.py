from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader
from .models import Candidate
import json
from django.core.paginator import Paginator

# list of mobile User Agents
mobile_uas = [
	'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
	'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
	'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
	'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
	'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
	'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
	'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
	'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
	'wapr','webc','winw','winw','xda','xda-'
	]
mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone' ]

def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''
    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]
    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True
                return mobile_browser

def index(request):
    '''Render the index page'''
    candidates = Candidate.objects.all().order_by('count')[0:10]
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

def index111(request):
    '''Render the index page'''
    candidates = Candidate.objects.all().order_by('count')[0:10]
    candidate_list = Candidate.objects.all()
    paginator = Paginator(candidate_list, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    if mobileBrowser(request):
        return render(request, 'elections/m_index.html', {
        'candidates':candidates, 'posts':posts
        })
    else:
        return render(request, 'elections/index.html', {
        'candidates':candidates, 'posts':posts
        })
