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

session = requests.Session()
#headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 8.6.2'}
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'}


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
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
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
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
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
    del tits[0]
    del counts[0]
    del days[0]
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
        # date_p = str(datetime.datetime.strptime(date_p, "%H:%M:%S"))
        date = str(datetime.datetime.now().year) + "-" + str('%02d' % datetime.datetime.now().month) + "-" + str(
            '%02d' % datetime.datetime.now().day) + " " + date_p
        # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
        temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
        temp_list.append(temp_dict)

    pages = soup.find(class_="pageN")
    a = pages.find_all('a')
    for page in a[0:1]:
        url = 'http://www.slrclub.com/' + page.get('href')
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
            # date_p = str(datetime.datetime.strptime(date_p, "%H:%M:%S"))
            date = str(datetime.datetime.now().year) + "-" + str('%02d' % datetime.datetime.now().month) + "-" + str(
                '%02d' % datetime.datetime.now().day) + " " + date_p
            # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
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
        #req = requests.get(url, headers=headers)
        req = requests.get(url)
        html = req.text
        soup = BS(html, "html.parser")
        #print(soup)
        time.sleep(3)
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
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
            temp_list.append(temp_dict)

    #toJson(temp_list)
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
            temp_dict = {'day': date, 'title': title, 'link': link}
            temp_list.append(temp_dict)

    # toJson(temp_list)
    return temp_list


'''  실행 '''

if __name__ == '__main__':
    Candidate.objects.all().delete()
    parsed_data = []
    parsed_data_ygosu = ygosu_parsing()
    parsed_data_ou = ou_parsing()
    parsed_data_slr = SLR_parsing()
    parsed_data_clien = clien_parsing()

    parsed_data.extend(parsed_data_ygosu)
    parsed_data.extend(parsed_data_ou)
    parsed_data.extend(parsed_data_slr)
    parsed_data.extend(parsed_data_clien)

    ''' 시간순 정렬 '''
    parsed_data = sorted(parsed_data, key=itemgetter('day'), reverse=1)
    toJson(parsed_data)

    for i in range(len(parsed_data)):
        new_candidate = Candidate(date=parsed_data[i]["day"],
                                  title=parsed_data[i]["title"],
                                  count=parsed_data[i]["count"],
                                  link=parsed_data[i]["link"]
                                  # image=parsed_data[i]["image"]
                                  )
        new_candidate.save()

''' 카테고리'''

hoobang.objects.all().delete()
parsed_data_hoobang = []
parsed_data_hoobang = ygosu_hoobang_parsing()
parsed_data_hoobang = sorted(parsed_data_hoobang, key=itemgetter('day'), reverse=1)
toJson_hoobang(parsed_data_hoobang)

for i in range(len(parsed_data_hoobang)):
    new_hoobang = hoobang(date=parsed_data_hoobang[i]["day"],
                          title=parsed_data_hoobang[i]["title"],
                          # count=parsed_data[i]["count"],
                          link=parsed_data_hoobang[i]["link"]
                          # image=parsed_data[i]["image"]
                          )
    new_hoobang.save()
