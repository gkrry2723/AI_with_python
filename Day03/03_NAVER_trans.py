import os
import sys
import urllib.request
import json

client_id = "gI_klQ1tw7B8qFubjP3_"
client_secret = "vRw7EJzfCv"

with open('index.txt','r',encoding='utf8') as f:
    srcText = f.read()


encText = urllib.parse.quote(srcText)
data = "source=en&target=ko&text=" + encText        #source 번역하고 싶은 언어 , target 번역 될 언어
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    res = json.loads(response_body.decode('utf-8'))
    from pprint import pprint
    pprint(res)

    with open('trans.txt', 'w', encoding='utf8') as f:
        f.write(res['messege']['result']['translatedText'])
    #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)