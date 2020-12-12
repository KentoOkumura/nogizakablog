# -*- coding: utf-8 -*-
import re
import os
import datetime
import requests
import lxml
from  bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0'}

#members = ['erika.ikuta', 'asuka.saito', 'minami.hoshino', 'fourth']
members = ['erika.ikuta', 'asuka.saito', 'minami.hoshino']

for i in members:
    url = "http://blog.nogizaka46.com/{}/".format(i)

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")

    title  = soup.find('h1', class_='clearfix').find('span', class_='entrytitle').text
    link   = soup.find('h1', class_='clearfix').find('span', class_='entrytitle').find('a').get('href')
    author = soup.find('span', class_='author').text
    year   = soup.find('div', class_='entrybottom').text.split('/')[0]
    month  = soup.find('div', class_='entrybottom').text.split('/')[1]
    day    = re.split('[ ｜]', soup.find('div', class_='entrybottom').text.split('/')[2])[0]
    hour   = re.split('[ :]', soup.find('div', class_='entrybottom').text.split('/')[2])[1]
    minute = re.split('[ :｜]', soup.find('div', class_='entrybottom').text.split('/')[2])[2]

    cur_day = datetime.datetime.now().strftime("%d")

    if not cur_day == day:
        continue

    filename = "/home/kento/work/nogizaka/{}.txt"
    filename = filename.format(i)

    if not os.path.isfile(filename):
        file = open(filename, 'w')
        file.close()
    
    file = open(filename, 'r')
    before_link = file.readline()
    file.close()

    file = open(filename, 'w')
    file.writelines(link)
    file.close()

    if not link == before_link:
        notifyUrl = "https://notify-api.line.me/api/notify"
        token = "DVj63kzTcqVtPcUqhBRzNOTwWrLIngWIIvorB3udCBN"
        apiHeaders = {"Authorization" : "Bearer "+ token}
        message =  title + " " + author + "\n" + link
        payload = {"message" :message}
        r = requests.post(notifyUrl ,headers = apiHeaders ,params=payload)
