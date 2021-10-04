import requests
import re
import urllib
import os
from bs4 import BeautifulSoup
import time
import random

from lxml import etree
base = 'http://www.mafengwo.cn'
url= 'http://www.mafengwo.cn/i/22027918.html'
header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'1631521805%3B%7D; UM_distinctid=17bde47290713a-0717485320c31c-f7f1939-144000-17bde472908f1b; uva=s%3A286%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222021-09-13%22%3Bs%3A2%3A%22lt%22%3Bi%3A1631521805%3Bs%3A10%3A%22last_refer%22%3Bs%3A159%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2g0OkaC5pLh_53PROHKmNe18ka_cYlpK37NHjNkz6rqhVPTsyTrQojZH83bjD90D8RO7zgAPnzXrc6NlAVBxwK%26wd%3D%26eqid%3Dd29e69930001aa4100000003613f0bfd%22%3Bs%3A5%3A%22rhost%22%3Bs%3A13%3A%22www.baidu.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1631521805%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=613f0c0d-c318-4b58-1fd0-ef572a0d84ba; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A21%3A%22https%3A%2F%2Fwww.baidu.com%22%3Bs%3A2%3A%22hp%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1026%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222021-09-27+14%3A52%3A38%22%3B%7D; __mfwothchid=referrer%7Cwww.baidu.com; __omc_chl=; __mfwc=referrer%7Cwww.baidu.com; __omc_r=; PHPSESSID=30r3jf9h2ulthn13cc4k9humu0; __mfwa=1631521810566.36067.6.1633066916682.1633224677409; __mfwlv=1633224677; __mfwvn=5; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1632725573,1633009666,1633066917,1633224678; __mfwb=af28c8251db6.23.direct; __mfwlt=1633228580; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1633228580'
,'Host':'www.mafengwo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
}
# url = base + '/search/q.php?q=%E5%9C%A3%E5%9C%B0%E5%B7%A1%E7%A4%BC&p={}&t=notes&kt=1'.format(page)
print(url)
def fixed_fun(js_con, url):
    func_return = js_con.replace('eval(', 'return(')

    content = execjs.compile(func_return)

    fn = js_con.split('=')[0].split(' ')[1]

    evaled_func = content.call(fn)

    fn = evaled_func.split('=')[0].split(' ')[1]  # 获取动态函数名

    aa = evaled_func.split("<a href=\\'/\\'>")  # 获取<a>标签的内容

    aa = aa[1].split("</a>")[0] if len(aa) >= 2 else ' '

    mode_func = evaled_func. \
        replace(
        "setTimeout('location.href=location.pathname+location.search.replace(/[\\?|&]captcha-challenge/,\\'\\')',1500);document.cookie=",
        'return').\
        replace(';if((function(){try{return !!window.addEventListener;}', ''). \
        replace(
        "}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded'," + fn + ",false)}else{document.attachEvent('onreadystatechange'," + fn + ")",
        ''). \
        replace(
        "if((function(){try{return !!window.addEventListener;}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded'," + fn + ",false)}else{document.attachEvent('onreadystatechange'," + fn + ")",
        ''). \
        replace("return'__jsl_clearance", "var window={};return '__jsl_clearance"). \
        replace(
        "var " + fn + "=document.createElement('div');" + fn + ".innerHTML='<a href=\\'/\\'>" + aa + "</a>';" + fn + "=" + fn + ".firstChild.href",
        "var " + fn + "='" + url + "'")

    try:
        content = execjs.compile(mode_func)

        cookies = content.call(fn)

        __jsl_clearance = cookies.split(';')[0]

        return __jsl_clearance
    except:

        return  None
# 获取cookies
def get_521(url, user_agent):#这步是获取浏览器返回的cookie值
    res = requests.get(url, timeout=10, headers=header)
    print(res.status_code)
    __jsluid_h = res.cookies

    print(__jsluid_h)

    print(res.text)

    __jsluid_h = str(__jsluid_h).split('Cookie ')[1].split(' for')[0]

    txt = ''.join(re.findall('<script>(.*?)</script>', res.text))

    if txt:

        __jsl_clearance = fixed_fun(txt, url)

        return (__jsluid_h, __jsl_clearance)
res = requests.get(url, headers=header)
res2=etree.HTML(res.text)
content=res2.xpath('//div[@class="_j_content_box"]//text()')
print("22")