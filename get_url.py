from __future__ import with_statement
from os import name
import re
from typing import Mapping
import requests
from fake_useragent import UserAgent
from lxml import etree
import pymysql
result_url=[]
nums=[]
def get_url_result(result_url,nums):
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
    headers=get_random_ua()
    url_temp='https://search.bilibili.com/all?keyword=%E5%9C%A3%E5%9C%B0%E5%B7%A1%E7%A4%BC&from_source=webtop_search&page='
    for i in range(4,7):
        print(f"获取地{i}页成功")
        headers['Host'] = 'www.bilibili.com'
        url=url_temp+str(i)
        r = requests.get(url)
        html_xpath = etree.HTML(r.text)
        result=html_xpath.xpath('//ul[@class="video-list clearfix"]/li/a/@href')
        for j in result:
            temp="https:"+j
            temp=temp.split("?")[0]
            result_url.append(temp)
            # print(f"获取地{i}页成功")
            response = requests.get(temp, headers=headers)
            response.encoding = 'utf-8'
            page_text = response.text  # 获取主页面
            ex_bv = 'https://www.bilibili.com/video/(.*?)/'
            # bv = re.findall(ex_bv, page_text)[0]
            # # "BV1A4411y7Yp": {"aid": 66628801
            # print(bv)
            # ex = '"{num}":{"aid":(.*?)'.format(num=bv)  # 通过正则获取aid
            # aid = re.findall(ex, page_text)[0]
            aid=re.findall(':\{"aid":(.*?),', page_text)[0]
            nums.append(aid)
    return result_url,nums
        # print(f"获取地{i}页成功")
        # // www.bilibili.com / video / BV1PV41147z6?from=search
# get_url_result(result_url=result_url)
# print("11")

# "BV1A4411y7Yp":{"aid":66628801,"bvid":"BV1A4411y7Yp",
