# -*- coding: utf-8 -*-
import requests
import json

url = 'http://restapi.amap.com/v3/bus/linename?offset=20&city=guangzhou&keywords=540%E8%B7%AF&language=zh&key=1d55ec451057366bda9ebe2352f82e6f&page=1&extensions=all&scode=e23e9e96e58467fb7f7daa5687288238&ts=1481770522211'
#url = 'http://restapi.amap.com/v3/bus/linename'
headers = {
	'Host': 'restapi.amap.com',
	'Accept': '*/*',
	'logversion': '2.0',
	'platinfo': 'product=sea&platform=iOS&sdkversion=3.1.0',
	'Connection': 'keep-alive',
	'x-info': 'H4sIAAAAAAAAAwGwAU/+Nlphl4SypRGFsUv7zEfrT/JyrwVqoDMDGndMDCgcTMAPxAnK7IRFwm9Ao03rxYo8yqkNaLdbaV1f+ISe1JCn9SNxhvhl5rTLBwn+6jhuvsU3C76Nb67CcDjug7CCMU7L8w4XyHwDhaskQINdaTrVaa51G07st3qXp+5lGAeEB6OUJb6pmbUBKDVzho+vOSOqdkI64/Wu33giLtnQUA2Vis47/HYOVoATYCwyjD9rzZrHFXn10Cero5ASxJa3zihpp9mPa1L8cHKw9PvPPZ5Sruuj6xk8TrgqRw9dRNDHGNbGWAZYebWAYK9Pkmfn/bJvchQ22hzd/jDCAJxQQ6gvKg9ZfwZl81p7SCrRXX+MSAmn2xTVFVYsIA1l/CYzJ0McTQC8oVI82tL0tKW8ClK5T5NlymIT9KK/yHrxmjOty/jC0OpDC6dYC2WJJqmFBEoz3aKBVnG9WHDWQtCf2Cj7TKsMnuUdbYnzzFeLmTwkbcyr2Z7nT7FExdO3GipY9HvAlcdxKrPTpLjUTDORBaW8S0xbeItUoNvPJYBv+FJOGLMJdxPbgb4r5+RKfBWjOztlLMgtqbABAAA=',
	'User-Agent': 'AMAP_SDK_iOS_Search_3.1.0',
	'Accept-Language': 'zh-cn',
	'Accept-Encoding': 'gzip,deflate',
	'Connection': 'keep-alive'
	}

headers_run = {
	'Host': 'nxxtapi.gzyyjt.net:9009',
	'Content-Type': 'application/json',
	'Accept': '*/*',
	'Connection': 'keep-alive',
	'Cookie': 'DYNSRV=s1',
	'User-Agent': 'src_201510_iOS_unionxxt/3.0.3 (iPhone; iOS 9.3.3; Scale/2.00)',
	'Accept-Language': 'zh-Hans-CN;q=1',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Length': '422'
	}
url_getrun = 'http://nxxtapi.gzyyjt.net:9009/xxt_api/bus/runbus/getByRouteAndDirection'
payload = {"sign":"BFB899F1CF926D2509A3CE8F6AC46BE3CC1ED80B","appid":"xxtGci01","timestamp":"1481787958985","data":"{\"routeId\":\"1110\",\"direction\":\"0\"}","reqpara":"{\"devtype\":1,\"speed\":\"0.0\",\"direc\":\"0.0\",\"versiontype\":4,\"uid\":14042,\"reserved\":\"iOS\",\"gpstime\":\"1481783578141\",\"devno\":\"BD4DB42F-1111-4EA3-8BF7-82A032B10D71\",\"version\":\"3.0.3\",\"lng\":113.3251610781745,\"lat\":23.13190629492595}"}
s = requests.Session()
re = s.get(url, headers=headers, stream=True)
re1 = s.post(url_getrun,stream=True, headers=headers, data=payload)
contents = re.json()
jsObj = json.dumps(contents,ensure_ascii=False ,indent=2)

f = open('bus.json', 'wb')
f.write(jsObj.encode('utf-8'))
f.close()

contents_run = re1.json()
jsObj = json.dumps(contents_run,ensure_ascii=False ,indent=2)

f = open('bus_run.json', 'wb')
f.write(jsObj.encode('utf-8'))
f.close()



