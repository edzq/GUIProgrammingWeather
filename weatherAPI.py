#! /usr/bin/python
# coding = utf-8
import urllib.request
import json

def GetWeatherInfo():
    ApiUrl= \
            "http://api.jisuapi.com/weather/query?appkey=YOURID"
    try:
        html=urllib.request.urlopen(ApiUrl)
        #读取并解码
        data=html.read().decode("utf-8")
        #将JSON编码的字符串转换回Python数据结构
        jsonArr=json.loads(data)
        #output result of json
        return jsonArr
    except:
        return None


