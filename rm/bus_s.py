# -*- coding: utf-8 -*-
import requests
import json
import time

headers = {
	'Host': 'wxbus.gzyyjt.net',
	'Upgrade-Insecure-Requests': '1',
	'Connection': 'keep-alive',
	'Accept-Encoding': 'gzip, deflate',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Cookie': 'JSESSIONID=8F70E1A8D269CD7BD1925AC6E4173DFF; route=fe9b13b33d88398957ee445b97555283; gzhUser=gh_342e92a92760; openId=ouz9Msz1ISCr3XuDLljot-DDwFbo; realOpenId=ouz9Msz1ISCr3XuDLljot-DDwFbo; WBSRV=s3',
	'Accept-Language': 'zh-cn',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.5.1 NetType/WIFI Language/zh_CN'
}
#身份认证地址
verify_url = 'http://wxbus.gzyyjt.net/wei-bus-app/route?nickName=&gzhUser=gh_342e92a92760&openId=ouz9Msz1ISCr3XuDLljot-DDwFbo'
#根据公交路数获取routeid的url
route_url = 'http://wxbus.gzyyjt.net/wei-bus-app/route/getByName'
route_payload = {'name':'B8'}
s = requests.Session()
res = s.get(verify_url, headers=headers)
route = s.post(route_url, data=route_payload, headers=headers)
route_id = route.json()[0]['i']
print 'route_id :' + route_id
#route_id = '2110'
bus_list_url = 'http://wxbus.gzyyjt.net/wei-bus-app/routeStation/getByRouteAndDirection/'+route_id+'/0'
bus_run_url = 'http://wxbus.gzyyjt.net/wei-bus-app/runBus/getByRouteAndDirection/'+route_id+'/0'

#bus_list_res = s.get(bus_list_url, headers=headers)
bus_list_res = s.get(bus_run_url, headers=headers)
#print bus_list_res.text
jsObj_buslst = bus_list_res.json()

#json数据处理
'''del jsObj_buslst["c"]
del jsObj_buslst["lt"]
del jsObj_buslst["ft"]
bus_station = []
for i in jsObj_buslst["l"]:
	bus_station.append(i["n"])
del jsObj_buslst["l"]
jsObj_buslst["station"] = bus_station'''

#t=1 普通 t=2 短线 t=9 快线
#jsObj = json.dumps(dict(jsObj_buslst),ensure_ascii=False, indent=2)
jsObj = json.dumps(jsObj_buslst,ensure_ascii=False, indent=2)
#print type(jsObj_buslst)
#jsObj = json.loads(jsObj_buslst)
print jsObj.encode('utf-8')
#bus_run_res = s.get(bus_run_url, headers=headers)
#print bus_run_res.json()

'''for i in range(len(jsObj_buslst)):
	bl_num = len(jsObj_buslst[i]["bl"])
	bbl_num = len(jsObj_buslst[i]["bbl"])
	if bl_num != 0:
		print "有" + str(bl_num) +"辆车靠近第" + str(i + 1) + "个站点。"
	elif bbl_num != 0:
		print "有" + str(bbl_num) +"辆车靠近第" + str(i + 1) + "个站点。"
	else:
		print "无运行车辆信息。"'''

