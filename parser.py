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

session = requests.Session()
# headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 8.6.2'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'}


def toJson(mnet_dict):
    with open('title_link.json', 'w', encoding='utf-8') as file:
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')


def toJson_hoobang(mnet_dict):
    with open('title_link_hoobang.json', 'w', encoding='utf-8') as file:
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')


def ygosu_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1, 2):
        url = 'https://www.ygosu.com/community/real_article?page={}' 'developers/what-http-headers-is-my-browser-sending'.format(
            page)
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BS(html, "html.parser")
        table = soup.find(class_="board_wrap")
        tits = table.find_all(class_="tit")
        counts = table.find_all(class_="read")
        days = table.find_all(class_="date")

        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = tit.a.get('href')
            '''
            ##image
            req = session.get(link, headers=headers)
            soup = BS(req.text, "html.parser")
            container = soup.find(class_='container')
            if container:
                if container.find('embed'):
                    embedtag = container.find('embed')
                    image = embedtag.get('src')
                elif container.find('img'):
                    imgtag = container.find('img')
                    image = imgtag.get('src')
                elif container.find('video'):
                    imgtag = container.find('video')
                    image = imgtag.get('src')
                else:
                    image = 'none'
            '''
            read = count.get_text()
            date_p = day.get_text()
            # date_p = str(datetime.datetime.strptime(date_p, "%H:%M:%S"))
            date = str(datetime.datetime.now().year) + "-" + str('%02d' % datetime.datetime.now().month) + "-" + str(
                '%02d' % datetime.datetime.now().day) + " " + date_p
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'source': '와고'}
            temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


def ou_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1, 2):
        url = 'http://www.todayhumor.co.kr/board/list.php?table=humorbest&page={}'.format(page)
        req = requests.get(url, headers=headers)
        time.sleep(10)
        html = req.text
        time.sleep(10)
        soup = BS(html, "html.parser")

        table = soup.find(class_="table_list")
        tits = table.find_all(class_="subject")
        counts = table.find_all(class_="hits")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = 'http://www.todayhumor.co.kr' + tit.a.get('href')
            '''
            # image
            req = session.get(link, headers=headers)
            soup = BS(req.text, "html.parser")
            container = soup.find(class_='viewContent')
            if container:
                if container.find('video'):
                    videotag = container.find('video')
                    image = videotag.get('poster')
                elif container.find('img'):
                    imgtag = container.find('img')
                    image = imgtag.get('src')
                else:
                    image = 'none'
                    '''

            read = count.get_text()
            date_p = day.get_text()
            date = str(datetime.datetime.strptime(date_p, "%y/%m/%d %H:%M"))
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'source': '오유'}
            temp_list.append(temp_dict)
    # toJson(temp_list)
    return temp_list


''' SLR 클럽 '''


def SLR_parsing():
    temp_dict = {}
    temp_list = []

    url = 'http://www.slrclub.com/bbs/zboard.php?id=best_article'
    req = requests.get(url, headers=headers)
    html = req.text
    soup = BS(html, "html.parser")
    tits = soup.find_all(class_="sbj")
    counts = soup.find_all(class_="list_click no_att")
    days = soup.find_all(class_="list_date no_att")

    for tit, count, day in zip(tits, counts, days):
        title = tit.a.get_text()
        link = 'http://www.slrclub.com/' + tit.a.get('href')
        '''
        ##image
        req = session.get(link, headers=headers)
        soup = BS(req.text, "html.parser")
        container = soup.find(class_='container')
        if container:
            if container.find('embed'):
                embedtag = container.find('embed')
                image = embedtag.get('src')
            elif container.find('img'):
                imgtag = container.find('img')
                image = imgtag.get('src')
            elif container.find('video'):
                imgtag = container.find('video')
                image = imgtag.get('src')
            else:
                image = 'none'
        '''
        read = count.get_text()
        date_p = day.get_text()
        date_p1 = day.get_text()
        date_p = str(datetime.datetime.now().year) + "-" + str(
            '%02d' % datetime.datetime.now().month) + "-" + str(
            '%02d' % datetime.datetime.now().day) + " " + date_p
        now = datetime.datetime.now()
        yesterday = now - timedelta(1)
        if (str(now) < date_p):
            date = str(datetime.datetime.now().year) + "-" + str(
                '%02d' % yesterday.month) + "-" + str(
                '%02d' % yesterday.day) + " " + date_p1
        else:
            date = str(datetime.datetime.now().year) + "-" + str(
                '%02d' % datetime.datetime.now().month) + "-" + str(
                '%02d' % datetime.datetime.now().day) + " " + date_p1
        temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'source': 'SLR'}
        temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


''' 클리앙 '''


def clien_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(0, 1):
        url = 'https://www.clien.net/service/group/clien_all?&od=T33&po={}'.format(
            page)

        req = requests.get(url, verify=False)
        # cookies = {'session_id': 'CDNSEC=e19a50f57ff50fc4b8485dd88ef59115'}
        # req = requests.get(url)
        #req = urllib.request.Request(url)
        #req = urllib.request.urlopen(req)
        html = req.text
        soup = BS(html, "html.parser")
        table = soup.find(class_="list_content")
        links = table.find_all(class_="list_subject")
        tits = table.find_all(class_="subject_fixed")
        counts = table.find_all(class_="hit")
        days = table.find_all(class_="timestamp")

        for link, tit, count, day in zip(links, tits, counts, days):
            title = tit.get('title')
            link = 'https://www.clien.net' + link.get('href')
            read = count.get_text()
            date = day.get_text()
            # date = str(datetime.datetime.strptime(date_p, "%y/%m/%d %H:%M"))
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'source': '클량'}
            temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


''' 보배드림 '''


def bobae_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1, 2):
        url = 'https://www.bobaedream.co.kr/list?code=best&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=&s_key=&level_no=&bestCode=&bestDays=&bestbbs=&vdate=&type=list&page={}'.format(
            page)

        req = requests.get(url, headers=headers, verify=False)
        #time.sleep(10)
        req.encoding = 'utf-8'
        html = req.text
        #time.sleep(10)
        soup = BS(html, "html.parser")

        table = soup.find(class_="clistTable02")
        tits = table.find_all(class_="pl14")
        counts = table.find_all(class_="count")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = 'https://www.bobaedream.co.kr' + tit.a.get('href')
            '''
            # image
            req = session.get(link, headers=headers)
            soup = BS(req.text, "html.parser")
            container = soup.find(class_='viewContent')
            if container:
                if container.find('video'):
                    videotag = container.find('video')
                    image = videotag.get('poster')
                elif container.find('img'):
                    imgtag = container.find('img')
                    image = imgtag.get('src')
                else:
                    image = 'none'
                    '''

            read = count.get_text()
            date_p = day.get_text()
            date_p1 = day.get_text()
            date_p = str(datetime.datetime.now().year) + "-" + str(
                '%02d' % datetime.datetime.now().month) + "-" + str(
                '%02d' % datetime.datetime.now().day) + " " + date_p
            now = datetime.datetime.now()
            yesterday = now - timedelta(1)
            if (str(now) < date_p):
                date = str(datetime.datetime.now().year) + "-" + str(
                    '%02d' % yesterday.month) + "-" + str(
                    '%02d' % yesterday.day) + " " + date_p1
            else:
                date = str(datetime.datetime.now().year) + "-" + str(
                    '%02d' % datetime.datetime.now().month) + "-" + str(
                    '%02d' % datetime.datetime.now().day) + " " + date_p1
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'source': '보배'}
            temp_list.append(temp_dict)
    # toJson(temp_list)
    return temp_list

''' 뽐뿌 '''
def ppomppu_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1, 2):
        url = 'http://www.ppomppu.co.kr/hot.php?id=&page={}'.format(
            page)
        req = requests.get(url, headers=headers, verify=False)
        html = req.text
        soup = BS(html, "html.parser")
        table = soup.find('table', class_='board_table')
        lines = table.find_all('tr', class_='line')
        # print(tits)
        # counts = 0
        # links = table.find_all(class_="bbsList")
        # days_p = table.find_all(class_="main_list_vote")
        # days = table.find_all('span', attrs={'class': 'not_exist'})
        # days = table.find_all(class_='board_date')

        # for tit, count, day in zip(tits, counts, days):
        for line in lines:
            title_p = line.find_all('td', align="left")
            title = title_p[1].a.get_text()
            link = 'http://www.ppomppu.co.kr' + title_p[1].a.get('href')
            read = 0
            date_p = line.find(class_='board_date').get_text()
            # date_p = str(datetime.datetime.strptime(date_p, "%H:%M:%S"))
            date = str(datetime.datetime.now().year) + "-" + str('%02d' % datetime.datetime.now().month) + "-" + str(
                '%02d' % datetime.datetime.now().day) + " " + date_p
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'source': '뽐뿌'}
            temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


''' 카테고리 '''


def ygosu_hoobang_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1, 2):
        url = 'https://www.ygosu.com/all_search/?type=board&add_search_log=Y&keyword=%E3%85%8E%E3%85%82&order=1&page={}' 'developers/what-http-headers-is-my-browser-sending'.format(
            page)
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BS(html, "html.parser")
        table = soup.find(class_="type_board2")
        tits = table.find_all(class_="subject")
        # counts = table.find_all(class_="read")
        days = table.find_all(class_="date")

        for tit, day in zip(tits, days):
            title = tit.get_text()
            link = tit.get('href')
            # read = count.get_text()
            date_p = day.get_text()
            date = str(datetime.datetime.strptime(date_p, "%Y-%m-%d"))
            # date = str(datetime.datetime.now().year) + "-" + str('%02d'%datetime.datetime.now().month) + "-" + str(
            #    '%02d'%datetime.datetime.now().day) + " " + date_p
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
            temp_dict = {'day': date, 'title': title, 'link': link, 'source': '와고'}
            temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


def DB_json():
    temp_dict = {}
    temp_list = []

    DB_data_all= Candidate.objects.all().values_list()

    for kk in range(0, len(DB_data_all)):
        title = Candidate.objects.all().values_list()[kk][2]
        link = Candidate.objects.all().values_list()[kk][4]
        date = Candidate.objects.all().values_list()[kk][1]
        count = Candidate.objects.all().values_list()[kk][3]
        source = Candidate.objects.all().values_list()[kk][5]
        temp_dict = {'day': date, 'title': title, 'link': link, 'count':count, 'source': source}
        temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


def DB_json_hoobang():
    temp_dict = {}
    temp_list = []

    DB_data_all= hoobang.objects.all().values_list()

    for kk in range(0, len(DB_data_all)):
        title = hoobang.objects.all().values_list()[kk][2]
        link = hoobang.objects.all().values_list()[kk][4]
        date = hoobang.objects.all().values_list()[kk][1]
        #count = hoobang.objects.all().values_list()[kk][3]
        source = hoobang.objects.all().values_list()[kk][5]
        temp_dict = {'day': date, 'title': title, 'link': link, 'source': source}
        temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list

'''  실행 '''

if __name__ == '__main__':
    parsed_data = []
    parsed_data_ygosu = ygosu_parsing()
    parsed_data_ou = ou_parsing()
    parsed_data_slr = SLR_parsing()
    parsed_data_clien = clien_parsing()
    parsed_data_ppomppu = ppomppu_parsing()
    parsed_data_bobae = bobae_parsing()

    parsed_data.extend(parsed_data_ygosu)
    parsed_data.extend(parsed_data_ou)
    parsed_data.extend(parsed_data_slr)
    parsed_data.extend(parsed_data_clien)
    parsed_data.extend(parsed_data_ppomppu)
    parsed_data.extend(parsed_data_bobae)


    ''' DB 읽기 '''
    json_data = DB_json()
    ''' 이전 파싱 데이터와 비교  이전에 없으면 append '''
    json_data_len = len(json_data)
    parsed_data_len = len(parsed_data)
    flag = 0
    for k in range(0, parsed_data_len):
        for j in range(0, json_data_len):
            if parsed_data[k]['link'] in json_data[j]['link']:
                flag = 1
        if flag == 0:
            json_data.append(parsed_data[k])
        else:
            flag = 0

    ''' 시간순 정렬 '''
    json_data = sorted(json_data, key=itemgetter('day'), reverse=1)

    ''' 최종 out 저장 '''
    toJson(json_data)

    Candidate.objects.all().delete()
    for i in range(len(json_data)):
        new_candidate = Candidate(date=json_data[i]["day"],
                                  title=json_data[i]["title"],
                                  count=json_data[i]["count"],
                                  link=json_data[i]["link"],
                                  source=json_data[i]["source"]
                                  # image=json_data[i]["image"]
                                  )
        new_candidate.save()





    ''' 후방주의 '''

    parsed_data_hoobang = []
    parsed_data_hoobang = ygosu_hoobang_parsing()
    parsed_data_hoobang = sorted(parsed_data_hoobang, key=itemgetter('day'), reverse=1)

    ''' DB 읽기 '''
    json_data_hoobang = DB_json_hoobang()
    ''' 이전 파싱 데이터와 비교  이전에 없으면 append '''
    json_data_hoobang_len = len(json_data_hoobang)
    parsed_data_hoobang_len = len(parsed_data_hoobang)
    flag = 0
    for k in range(0, parsed_data_hoobang_len):
        for j in range(0, json_data_hoobang_len):
            if parsed_data_hoobang[k]['link'] in json_data_hoobang[j]['link']:
                flag = 1
        if flag == 0:
            json_data_hoobang.append(parsed_data_hoobang[k])
        else:
            flag = 0

    ''' 최종 out 저장 '''
    json_data_hoobang = sorted(json_data_hoobang, key=itemgetter('day'), reverse=1)
    toJson_hoobang(json_data_hoobang)

    hoobang.objects.all().delete()
    for i in range(len(json_data_hoobang)):
        new_hoobang = hoobang(date=json_data_hoobang[i]["day"],
                              title=json_data_hoobang[i]["title"],
                              # count=json_data[i]["count"],
                              link=json_data_hoobang[i]["link"],
                              # image=json_data[i]["image"]
                              source=json_data_hoobang[i]["source"]
                              )
        new_hoobang.save()
