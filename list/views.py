from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader
from elections.models import Candidate
from hoobang.models import hoobang
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



def index(request):
	candidates = Candidate.objects.all().order_by('-date')[0:10]
	hoobangs = hoobang.objects.all().order_by('-date')[0:10]
	return render(request, 'list/index.html', {'candidates':candidates, 'hoobangs':hoobangs})



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
