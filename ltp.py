import requests
import json
API_ENDPOINT = "https://shoonyabrd.finvasia.com/DataPub/api/SData/LiveFeed"


def get_ltp(token):
    data={"Count":1,
    "Data":"{SecIdxCode:-1,Exch:1,ScripIdLst:["+str(token)+"],Seg:2}",
    "DoCompress":False,
    "RequestCode":146,
    "Reserved":"FVSA147",
    "Source":"W",
    "UserId":"",
    "UserType":"C"}
    r = requests.post(url = API_ENDPOINT, data = data)
    json_data=json.loads(r.text)
    return int(json_data[0]['fLastTradedPrice'])