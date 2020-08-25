
import os
import sys
import urllib.request
import json
from pprint import pprint
#########################################################################################################
# 1. 팀: 유채림 조
# 2. 날짜: 2020.08.25 (3일차)
# 2. 팀원: 20184754 김현주, 20184487 유채림
# 3. mission 내용: naver open API를 이용하기!
#                 사용자가 원하는 검색어를 2개 입력하면 2020-01-01 부터 2020-08-01 까지 검색 rate를 반환해 준다.
#########################################################################################################




client_id = "gI_klQ1tw7B8qFubjP3_"
client_secret = "vRw7EJzfCv"

print("검색량 데이터 조회 서비스에 오신걸 환영합니다!")
txt = str(input("검색어 1을 입력하세요 : "))
txt = "\""+txt+"\""         # open API 양식에 맞도록 입력 value 수정

txt2 = str(input("검색어 2를 입력하세요 : "))
txt2 = "\""+txt2+"\""       # open API 양식에 맞도록 입력 value 수정

url = "https://openapi.naver.com/v1/datalab/search" #open API
body = "{\"startDate\":\"2020-01-01\",\"endDate\":\"2020-08-01\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"검색어\",\"keywords\":["+txt+","+txt2+"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"],\"gender\":\"f\"}"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    face = json.loads(response_body)
    pprint(face)
    #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)