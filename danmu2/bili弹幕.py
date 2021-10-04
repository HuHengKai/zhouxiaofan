from __future__ import with_statement
from os import name
import random
import re,time
from typing import Mapping
import requests
from fake_useragent import UserAgent
from lxml import etree
import pymysql
from 获取url import get_url_result
# 获取urls
result_url=[]
result_urls=get_url_result(result_url)
# 获取数据库
db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='bilibili')
cursor = db.cursor()
def insert(values):
    sql = "INSERT INTO danmu(content,url) values(%s,%s)"
    try:
        cursor.execute(sql, values)
        db.commit()
    except:
        db.rollback()
        print("插入数据失败")


# 获取随机头信息
def get_random_ua():
    try:
        ua = UserAgent.chrome
    except:
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
    headers = {
        'Host': '',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': ua,
        'cache-control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'pragma': 'no-cache',
        'Referer': 'https://www.bilibili.com/'
    }
    return headers


# 获取播放页面源码
def get_page_source(url, headers):
    headers['Host'] = 'www.bilibili.com'
    r = requests.get(url, headers=headers)
    return r.text


# 从页面源码中分析得出 cid 编号，即弹幕的 xml 文件地址
def get_cid(page_source):
    cid = re.findall('cid=(.*?)&aid=', page_source)[0]
    return cid


# 获取弹幕
def get_comment(xml_url, headers):
    headers['Host'] = 'comment.bilibili.com'
    r = requests.get(xml_url, headers=headers)
    html_xpath = etree.HTML(r.content)
    comment_list = html_xpath.xpath('//d/text()')
    return comment_list


# 主函数
def main():
    url_list = [
        'https://www.bilibili.com/video/BV1b4411S7d1',
    ]
    # 'https://www.bilibili.com/video/BV1qK41157Eq?from=search
    result_url = []
    result_urls = get_url_result(result_url)
    for url in result_urls:
        a = random.randrange(2,10, 1)
        print(url)
        time.sleep(a)
        if '?' in url:
            url = re.findall('(.*?)\?', url)[0]

        headers = get_random_ua()
        page_source = get_page_source(url, headers)
        cid = get_cid(page_source)
        xml_url = 'https://comment.bilibili.com/' + cid + '.xml'

        comment = get_comment(xml_url, headers)
        # 如果想获取去重后的使用这个
        # comment = set(get_comment(xml_url,headers))

        for i in comment:
            temp=[]
            temp.append(i)
            temp.append(url)
            # insert(temp)
            with open('弹幕110.txt', 'a', encoding='utf-8') as f:
                temps=i+"？？？？？？？？？？"+str(url)
                f.write(temps + '\n')
            f.close()


if __name__ == '__main__':
    main()

    cursor.close()
    db.close()
