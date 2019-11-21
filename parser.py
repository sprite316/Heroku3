import os
import urllib

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django

django.setup()

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import json
import schedule
import time
import requests
from elections.models import Candidate


session = requests.Session()
#headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 8.6.2'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def toJson(mnet_dict):
    with open('title_link.json', 'w', encoding='utf-8') as file:
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')


def ygosu_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1, 8):
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

                read = count.get_text()
                date = day.get_text()
                temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
                # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
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
        print(soup)
        table = soup.find(class_="table_list")
        tits = table.find_all(class_="subject")
        counts = table.find_all(class_="hits")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):

            title = tit.a.get_text()
            link = 'http://www.todayhumor.co.kr' + tit.a.get('href')

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

                read = count.get_text()
                date = day.get_text()
                temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
                # temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
                temp_list.append(temp_dict)
    # toJson(temp_list)
    return temp_list


if __name__ == '__main__':
    Candidate.objects.all().delete()
    parsed_data = []
    parsed_data = ygosu_parsing()
    #parsed_data1 = ou_parsing()
    #parsed_data.extend(parsed_data1)
    toJson(parsed_data)

    for i in range(len(parsed_data)):
        new_candidate = Candidate(date=parsed_data[i]["day"],
                                  title=parsed_data[i]["title"],
                                  count=parsed_data[i]["count"],
                                  link=parsed_data[i]["link"],
                                  image=parsed_data[i]["image"]
                                  )
        new_candidate.save()
