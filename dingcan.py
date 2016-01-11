#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import requests

url      = "http://dingcan.***.com/index.php?m=login&a=in"
url1     = "http://dingcan.***.com/index.php"
url2     = "http://dingcan.***.com/index.php?m=dingcan&a=dinner"
headers  = {"Host":"dingcan.***.com","Referer":"http://dingcan.***.com"}
s        = requests.Session()
r        = s.get(url1,headers = headers)
pattern  = re.compile('<input.*?name="__hash__".*?value="(.*?)" />',re.S)
items    = re.findall(pattern,r.text)
data     = {"username":"***","password":"***","__hash__":items[0]}

resp     = s.post(url,data = data,headers = headers)#模拟发送post登录请求

r1       = s.get(url2,headers = headers)
pattern1 = re.compile('<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>.*?<input.*?name="(.*?)".*?value="(.*?)".*?</td>.*?</tr>',re.S)
items1   = re.findall(pattern1,r1.text)
i        = 0
data2    = {}
sel_cai  = ''
for item in items1:
    if(i==0):
        print "餐馆：",item[0]
    print "菜品：",item[1],item[2]
    data2[item[2]] = "0"
    if(item[3] != '0'):
        sel_cai = item[1]+" "+item[2]
    i+=1

#判断是否之前已定过餐
if(len(sel_cai) > 0):
    print "\033[36m已选菜品\033[0m：",sel_cai

pattern2 = re.compile('<input.*?name="__hash__".*?value="(.*?)" />',re.S)
__hash__ = re.findall(pattern2,r1.text)
get_id   = raw_input("-------------------------------请根据下面提示选择菜品--------------------------------\n(填写后面的数字即可,0退出订餐,c取消订餐,多选请用\033[31m|\033[0m隔开,\033[32;49;1m 每次重定会覆盖之前的,请认真核对 \033[39;49;0m)：")
if(get_id == "0"):
    print '你已退出订餐'
    exit()
elif(get_id == "c"):
    #取消之前的订餐,什么都不执行(此处随便加了一句,什么都不写会报错,菜鸟不知道怎么避免这个报错)
    a = 1 
else:
    ids = get_id.split('|')
    for i in ids:
        #防止用户输入有误，提交错误的数据
        if(data2.has_key(i)):
            data2[i] = 1
data2["__hash__"]  = __hash__[0]
data2["do_submit"] = "保存"
resp2              = s.post(url2,data = data2,headers = headers)#提交订餐内容
if(resp2.status_code == 200):
    print '保存成功'
else:
    print '保存失败，请重试'
