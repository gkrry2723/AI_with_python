import os
import sys
import requests
import json
from pprint import pprint
client_id = "gI_klQ1tw7B8qFubjP3_"
client_secret = "vRw7EJzfCv"

#url = "https://openapi.naver.com/v1/vision/face" # 얼굴 인식
url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식

files = {'image': open('photo_0.JPG', 'rb')}     #내가 가지고 있는 IMAGE 경로
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
if(rescode==200):
    face = json.loads(response.text)
    pprint(face)
    #print (response.text)
else:
    print("Error Code:" + rescode)