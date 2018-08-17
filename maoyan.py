# !/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
import time
import json
from requests.exceptions import RequestException

def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return  None

# 定义parse_one_page，对html进行解析,re.S表示匹配任何非空白字符，其中（.*？)表示匹配的内容：
def parse_one_page(html):
      pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a'
                           +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                            +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)

       #html表示匹配的目标对象
      items= re.findall(pattern, html)
      for item in items:
          yield {
              "index":item[0],
              "image":item[1],
              "name":item[2],
              "actor":item[3].strip(),
              "time":item[4].strip(),
              "star":item[5]+item[6],
       }

def main(offset):
     url = 'http://maoyan.com/board/4?offset='+ str(offset)
     html = get_one_page(url)
     for item in parse_one_page(html):
         print(item)
         # write_to_file(item)
         write_to_csv(item)

def write_to_csv(content):
    with open("猫眼result.csv",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) +'\n')

# def write_to_file(content):
#     # a表示追加的方式进行添加
#     with open('猫眼result.txt', 'a', encoding='utf-8') as f:
#         f.write(json.dumps(content, ensure_ascii=False) + '\n')




if __name__ =="__main__":
   for i in range(10):
       main(offset = i * 10)
       time.sleep(1)