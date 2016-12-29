# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash ,request
from flask_bootstrap import Bootstrap
from forms import BusNum
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import requests
from . import main
from ..models import Bus
import re

@main.route('/', methods=['GET', 'POST'])
def index():
	form = BusNum()
	if form.validate_on_submit():
		if form.num.data == None:
			flash('请输入车辆信息')
		num = form.num.data.upper()
		return redirect(url_for('main.runbus_status', busnum=num, direction='0'))
	return render_template('index.html', form=form)

@main.route('/runbus/<busnum>/<direction>')
def runbus_status(busnum, direction):
	busnum_s = busnum + u'路'
	status = Bus.query.filter_by(bus_num=busnum_s, direction=direction).first().bus
	buslist = status.replace('[','').replace(']','').replace('\'','').split(',')
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
	route_payload = {'name':busnum}
	s = requests.Session()
	res = s.get(verify_url, headers=headers)
	route = s.post(route_url, data=route_payload, headers=headers)
	route_id = route.json()[0]['i']
	run_bus_url = 'http://wxbus.gzyyjt.net/wei-bus-app/runBus/getByRouteAndDirection/'+route_id+ '/' + direction
	run_bus_res = s.get(run_bus_url, headers=headers)
	runbus = run_bus_res.json()
	return render_template('runbus.html', busnum=busnum, buslist=buslist, runbus=runbus, direction=direction)

@main.route('/runbus/reverse')
def bus_reverse():
	url = str(request.path)
	direction = url[-1:]
	busnum = re.findall('/runbus/(.*)/', url)
	print busnum
	if direction == '0':
		return redirect(url_for(runbus_status(busnum=busnum, direction='1')))
	if direction == '1':
		return redirect(url_for(runbus_status(busnum=busnum, direction='0')))
