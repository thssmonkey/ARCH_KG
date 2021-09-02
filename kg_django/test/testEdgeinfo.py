
import requests
import json
from django.http import HttpResponse

def getEdgeinfo():
    name1 = "扎克伯格"
    name2 = "文继荣"

    url = "http://websensor.playbigdata.com/fss3/service.svc/GetSearchResults"

    querystring = {"query": name1 + " " + name2, "num": "5", "start": "1"}

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'upgrade-insecure-requests': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'cache-control': "no-cache",
        'postman-token': "5549dc28-2253-f247-d5f9-1f8e87bd830f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)
    res = json.loads(response.text)
    response = HttpResponse(json.dumps(res), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

getEdgeinfo()