#-*- coding: utf-8 -*-
import os

import sys

import requests

import pprint



client_id = "zJKSgg5Whn0Iz1NJZXLb"

client_secret = "kZK1w3EsN6"

encText = "선별진료소"

 

url = "https://openapi.naver.com/v1/search/local.json?query=" + encText + "&display=5"

 

header_params = {"X-Naver-Client-Id":client_id,'X-Naver-Client-Secret': client_secret}

res = requests.get(url, headers = header_params)

 

if res.status_code == 200:

    data = res.json()

    item_list = data['items']

else:

    print("Error Code:" + str(res.status_code))

 

new_list = []

no = 0

 

for item in item_list:
    no += 1
    new_list.append([item['title'],item['roadAddress'],item['link']])

 

for item in new_list:



    print(str(no),'. ',item[0])

    print('주소:',item[1])

    print(item[2])


# import os

# import sys

# import urllib.request

 

# client_id = "zJKSgg5Whn0Iz1NJZXLb" # 개발자센터에서 발급받은 Client ID 값

# client_secret = "kZK1w3EsN6" # 개발자센터에서 발급받은 Client Secret 값

 

# encText = urllib.parse.quote("선")

# #data = "source=ko&target=en&text=" + encText  # source에서 target으로 바꾼다
# data = encText

# url = "https://openapi.naver.com/v1/search/local.json?query=" + data

# request = urllib.request.Request(url)

 

# request.add_header("X-Naver-Client-Id",client_id)

# request.add_header("X-Naver-Client-Secret",client_secret)

# response = urllib.request.urlopen(request, data=data.encode("utf-8"))

# rescode = response.getcode()

 

# if(rescode==200):

#     response_body = response.read()

#     print(response_body.decode('utf-8'))

# else:

#     print("Error Code:" + rescode)   