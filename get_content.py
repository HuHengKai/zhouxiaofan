#coding=utf-8
from get_url import get_url_result
import requests
import re
import time
import random
import emoji,re
# 存储函数
def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
def get_content(url,oid,i2):
    status=0
    response = requests.get(url, headers=headers)
    print("*"*20)
    print(url)
    response.encoding = 'utf-8'
    if len(response.text)>3000:
        print(url)
        data_json = response.json()
        replies_count = data_json['data']['cursor']['all_count']
        print('评论总数：' + str(replies_count))
        if data_json['data']['replies'] !=None:
            page = 1
            replies = data_json['data']['replies']
            for rep in replies:
                time.sleep(2)
                uname = rep['member']['uname']
                # 相关回复xx条
                # print(uname + ':' + rep['content']['message'] + '(' + rep['reply_control']['sub_reply_title_text'] + ')')
                content_temp=uname + ':'+rep['content']['message']
                content_temp=filter_emoji(content_temp)
                print(content_temp)
                if "\n" in content_temp:
                   content_temp=content_temp.replace("\n"," ")
                content_up=uname + '::' +uname+'::' + content_temp+"::"+str(i2)
                print(content_up)
                rep_replies = rep['replies']
                if rep_replies != None:
                    # 获取该评论下详细回复

                    with open('评论5.txt', 'a', encoding='utf-8') as f:
                        f.write(content_up + '\n')
                    f.close()
                    replies_url = 'https://api.bilibili.com/x/v2/reply/reply?pn={page}&type=1&oid={oid}&ps=10&root={root}'
                    root = rep_replies[0]['root']
                    # print(root)
                    replies_url = replies_url.format(page=page,root=root,oid=oid)
                    # print(replies_url)
                    time.sleep(1)
                    reply_response = requests.get(replies_url, headers=headers)
                    reply_json = reply_response.json()
                    list_reply = reply_json['data']['replies']
                    count = reply_json['data']['page']['count']
                    size = reply_json['data']['page']['size']
                    print(f"count is{count},size is{size}")
                    if count/size == 0:
                        page_num = count/size
                    else:
                        page_num = count//size + 1
                    for li in list_reply:
                        temp=li['member']['uname'] + "::" + '回复' + '  ' + uname + '::' + li['content']['message']
                        temp=filter_emoji(temp)+"::"+str(i2)
                        print(temp)
                        if "\n" in temp:
                            temp = temp.replace("\n", " ")
                        with open('评论5.txt', 'a', encoding='utf-8') as f:
                            f.write(temp + '\n')
                        f.close()
                    if count > size:
                        print("*"*20)
                        for pn in range(page + 1, page_num + 1):
                            replies_url = replies_url.replace('pn=' + str(pn - 1), 'pn=' + str(pn))
                            print(replies_url)
                            reply_response_pn = requests.get(replies_url, headers=headers)
                            reply_json_pn = reply_response_pn.json()
                            list_reply_pn = reply_json_pn['data']['replies']
                            if len(reply_response_pn.text) > 4500:
                                for list_pn in list_reply_pn:
                                        temp2=list_pn['member']['uname'] + "::" + '回复' + '    ' + uname + '::' + list_pn['content'][
                                            'message']
                                        temp2 = filter_emoji(temp2)+"::"+str(i2)
                                        if "\n" in temp2:
                                            temp2 = temp2.replace("\n", " ")
                                        with open('评论5.txt', 'a', encoding='utf-8') as f:
                                            f.write(temp2 + '\n')
                                        f.close()
                                        print("222")
                                        break
                    else:
                        print('结束爬取')

                            # for list_pn in list_reply_pn:
                            #     temp2=list_pn['member']['uname'] + "   " + '回复' + '    ' + uname + ':' + list_pn['content']['message']
                            #     with open('评论2.txt', 'a', encoding='utf-8') as f:
                            #         f.write(temp2 + '\n')
                            #     f.close()
                if rep_replies == None:
                    print("当前为一条")
                    with open('评论12.txt', 'a', encoding='utf-8') as f:
                        f.write(content_up + '\n')
                    f.close()
        else:
            print('结束爬取')
    else:
        print("爬取结束")
        status=1
    return status
if __name__ == '__main__':
    #BV1oL411E7eR
    # 1632800332089
    # start_url = 'https://www.bilibili.com/video/BV1MN41197rS?from=search&seid=3010064547294930064&spm_id_from=333.337.0.0'
    result=[]
    nums=[]
    result_url,nums_oid=get_url_result(result,nums)
    urls=[]
    for i in range(0,60):
        url="https://api.bilibili.com/x/v2/reply/main?next="+str(i)+'&type=1&oid={oid}&mode=3&plat=1'
        urls.append(url)
    for j in range(len(result_url)):
        i2=result[j]
        aid=str(nums[j])
        for url in urls:
            print(url)
            time.sleep(5)
            url = url.format(oid=aid)
            print(url)
            status2=get_content(url=url,oid=aid,i2=i2)
            if status2==1:
                break
# https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=1&type=1&oid=63528099&ps=10&root=1874191716&_=1632810828430
