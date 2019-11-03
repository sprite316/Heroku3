import os
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import json


def ou_parsing():
    temp_dict = {}
    temp_list = []

    for page in range(1,2):
        fullurl = 'http://www.todayhumor.co.kr/board/list.php?table=humorbest&page={}'.format(page)
        #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        headers = {'User-Agent':'Chrome/66.0.3359.181'}
        url = urllib.request.Request(fullurl, headers=headers)
        html = urlopen(url)
        source = html.read()
        html.close()
        soup = BS(source, "html.parser")
        print(soup)
        table = soup.find(class_="table_list")
        tits = table.find_all(class_="subject")
        counts = table.find_all(class_="hits")
        days = table.find_all(class_="date")
        for tit, count, day in zip(tits, counts, days):
            title = tit.a.get_text()
            link = 'http://www.todayhumor.co.kr'+tit.a.get('href')
            #image
            #url = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            #html = urlopen(url)
            #source = html.read()
            #html.close()
            #soup = BS(source, "html.parser")
            #container = soup.find(class_='viewContent')
            #if container.find('video'):
            #    videotag = container.find('video')
            #    image =videotag.get('poster')
            #if container.find('img'):
            #    imgtag = container.find('img')
            #    image =imgtag.get('src')
            #
            read = count.get_text()
            date = day.get_text()
            temp_dict = {'day': date, 'title': title, 'count': read, 'link': link}
            temp_list.append(temp_dict)
    #toJson(temp_list)
    return temp_list

ou_parsing()
