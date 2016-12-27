# -*- coding: utf-8 -*-
import requests
import json
import time
import sqlite3
# 导入:
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#模拟微信客户端header
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

#json数据处理函数,返回json信息
def json_data(jsdata):
	del jsdata["c"]
	del jsdata["lt"]
	del jsdata["ft"]
	bus_station = []
	for i in jsdata["l"]:
		bus_station.append(i["n"])
	del jsdata["l"]
	jsdata["station"] = bus_station
	#返回处理后的json数据
	return jsdata

def login(headers):
	#身份认证地址
	verify_url = 'http://wxbus.gzyyjt.net/wei-bus-app/route?nickName=&gzhUser=gh_342e92a92760&openId=ouz9Msz1ISCr3XuDLljot-DDwFbo'
	#获取带session的登陆信息
	s = requests.Session()
	s.get(verify_url, headers=headers)
	return s

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Bus(Base):
	# 表的名字:
	__tablename__ = 'bus'

	# 表的结构:
	id = Column(Integer, primary_key=True)
	bus_num = Column(String(20))
	route_id = Column(String(5))
	direction = Column(String(1))
	bus = Column(String(2000))

#数据库初始化函数
def init_db():
	Base.metadata.create_all(engine)

#抓取函数
def grab(s, routeid, headers, bus_list_url, session):
	#获取公交车站点的url，0,1两个方向
	bus_list_url0 = 'http://wxbus.gzyyjt.net/wei-bus-app/routeStation/getByRouteAndDirection/' + routeid + '/0/'
	bus_list_url1 = 'http://wxbus.gzyyjt.net/wei-bus-app/routeStation/getByRouteAndDirection/' + routeid + '/1/'
	#第一个方向
	print "grabing route id = " + routeid + ',direction = 0.'
	bus_list_res0 = s.get(bus_list_url0, headers=headers)
	try:
		jsObj_buslst0 = bus_list_res0.json()
		bus_info0 = json_data(jsObj_buslst0)
		#写入数据库
		new_bus0 = Bus(bus_num=bus_info0["rn"], route_id=routeid, direction='0', bus=str(bus_info0["station"]).replace('u\'','\'').decode('unicode-escape'))
		session.add(new_bus0)
		session.commit()
	except Exception as e:
		print e

	#第二个方向
	print "grabing route id = " + routeid + ',direction = 1.'
	bus_list_res1 = s.get(bus_list_url1, headers=headers)
	try:
		jsObj_buslst1 = bus_list_res1.json()
		bus_info1 = json_data(jsObj_buslst1)
		#写入数据库
		new_bus1 = Bus(bus_num=bus_info1["rn"], route_id=routeid, direction='1', bus=str(bus_info1["station"]).replace('u\'','\'').decode('unicode-escape'))
		session.add(new_bus1)
		session.commit()
	except Exception as e:
		print e

# 初始化数据库连接:
engine = create_engine('sqlite:///businfo.db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 初始化数据库
init_db()
session = DBSession()

bus_list_url = 'http://wxbus.gzyyjt.net/wei-bus-app/routeStation/getByRouteAndDirection/'

#获取包含cookie的登陆会话
s = login(headers)
#抓取routeid从1到1200范围内对应的公交站点信息
for i in range(485,1200):
	grab(s, str(i), headers, bus_list_url, session)
	#等待0.5s后再循环，太快的话服务器会拒绝连接
	time.sleep(0.5)

#提交数据库内容更改
#session.commit()
#关闭数据库连接会话
session.close()

