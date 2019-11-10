import os
import urllib
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import json

from elections.models import Candidate
Candidate.objects.all().delete()

def toJson(mnet_dict):
    with open('title_link.json', 'w', encoding='utf-8') as file:
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')

def ygosu_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1,8):
        url = 'https://www.ygosu.com/community/real_article?page={}'.format(page)
        html = urlopen(url)
        source = html.read()
        html.close()

        soup = BS(source, "html.parser")
        table = soup.find(class_="board_wrap")
        tits = table.find_all(class_="tit")
        counts = table.find_all(class_="read")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = tit.a.get('href')
            #image
            html = urlopen(link)
            source = html.read()
            html.close()
            soup = BS(source, "html.parser")
            container = soup.find(class_='container')
            if container.find('embed'):
                embedtag = container.find('embed')
                image =embedtag.get('src')
            elif container.find('img'):
                imgtag = container.find('img')
                image =imgtag.get('src')
            elif container.find('video'):
                imgtag = container.find('video')
                image = imgtag.get('src')
            else:
                image = 'none'
            #
            read = count.get_text()
            date = day.get_text()
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_list.append(temp_dict)
    #toJson(temp_list)
    return temp_list
'''
def ou_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1,8):
        fullurl = 'http://www.todayhumor.co.kr/board/list.php?table=humorbest&page={}'.format(page)
        url = urllib.request.Request(fullurl, headers={'user-agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Accept-Charset': 'utf-8'})
        html = urlopen(url)
        source = html.read()
        html.close()
        soup = BS(source, "html.parser")
        #print(soup)
        table = soup.find(class_="table_list")
        tits = table.find_all(class_="subject")
        counts = table.find_all(class_="hits")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = 'http://www.todayhumor.co.kr'+tit.a.get('href')
            url = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(url)
            source = html.read()
            html.close()
            soup = BS(source, "html.parser")
            container = soup.find(class_='viewContent')
            if container.find('video'):
                videotag = container.find('video')
                image =videotag.get('poster')
            elif container.find('img'):
                imgtag = container.find('img')
                image =imgtag.get('src')
            else:
                image = 'none'
            #
            read = count.get_text()
            date = day.get_text()
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link, 'image': image}
            temp_list.append(temp_dict)
    #toJson(temp_list)
    return temp_list
'''
if __name__=='__main__':
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
        image=parsed_data[i]["image"])
        new_candidate.save()
