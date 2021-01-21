import os

import sys

import requests

import pprint

 

client_id = "zJKSgg5Whn0Iz1NJZXLb"

client_secret = "kZK1w3EsN6"

encText = "마스크"

 

url = "https://openapi.naver.com/v1/search/shop.json?query=" + encText + "&display=50&sort=asc"

 

header_params = {"X-Naver-Client-Id":client_id,'X-Naver-Client-Secret': client_secret}

res = requests.get(url, headers = header_params)

 

if res.status_code == 200:

    data = res.json()

   # pprint.pprint(data)

    item_list = data['items']

else:

    print("Error Code:" + rescode)

    

num = 0

no = 0

new_list = []

 

for item in item_list:

    if item['category1']=='생활/건강':

        if int(item['productType']) < 4:

            num += 1

            if num <= 10:          

                new_list.append(item['title'].replace('<','').replace('b','').replace('>',''))

                new_list.append(item['link'])

                

for item in new_list:

   # no += 1

    #print(no)

    print(item)
