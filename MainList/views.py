from django.shortcuts import render
from HotList.models import HotList
from django.db.models import Q

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
    HotLists = HotList.objects.all().order_by('-date')[0:10]
    HoobangLists = HotList.objects.filter(
        Q(title__icontains='ㅎㅂ') | Q(title__icontains='후방') | Q(title__icontains='맥심') | Q(title__icontains='섹스') | Q(
            title__icontains='19금') | Q(title__icontains='ㅅㅅ') | Q(title__icontains='신재은') | Q(
            title__icontains='노출') | Q(title__icontains='도끼') | Q(title__icontains='조공'))
    HoobangLists = HoobangLists.order_by('-date')[0:10]
    return render(request, 'MainList/index.html', {'HotLists': HotLists, 'HoobangLists': HoobangLists})
