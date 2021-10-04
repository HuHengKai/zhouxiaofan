import requests
import re
import urllib
import os
from bs4 import BeautifulSoup
import time
import random
from lxml import etree
base = 'http://www.mafengwo.cn'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
           }
def geturl(): #从初始页面获取全部的次一级游记链接

    nextlink = []
    # https://www.mafengwo.cn/search/q.php?q=%E5%9C%A3%E5%9C%B0%E5%B7%A1%E7%A4%BC&p=2&t=notes&kt=1
    for page in range(1,3):

        url = base + '/search/q.php?q=%E5%9C%A3%E5%9C%B0%E5%B7%A1%E7%A4%BC&p={}&t=notes&kt=1'.format(page)
        print(url)

        res = requests.get(url, headers=headers)
        res2=etree.HTML(res.text)
        urls=res2.xpath('//div[@class="ct-text "]/h3/a/@href')
        titlelinks =[]

        for titlelink in urls:

            next = base + titlelink.find('a', class_='title-link').get('href') + '@' + titlelink.find('span',class_='comment-date').text

            print(next)

            nextlink.append(next)

        print(page)
    #print(nextlink)
    return nextlink
geturl()