# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os
import requests
def make_shell_context():
	return dict(app=app, db=db, Bus=Bus)


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite:///businfo.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
# 定义User对象:
class Bus(db.Model):
	# 表的名字:
	__tablename__ = 'businfo'

	# 表的结构:
	id = db.Column(db.Integer, primary_key=True)
	bus_num = db.Column(db.String(20))
	route_id = db.Column(db.String(5))
	direction = db.Column(db.String(1))
	bus = db.Column(db.String(2000))

	def __repr__(self):
		return '<Bus %r>' % self.bus_num

class BusNum(Form):
	num = StringField(u'公交路数', validators=[Required()])
	submit = SubmitField(u'查询')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = BusNum()
	if form.validate_on_submit():
		if form.num.data == None:
			flash('请输入车辆信息')
		num = form.num.data
		return redirect(url_for('runbus_status', busnum=num, direction='0'))
	return render_template('index.html', form=form)

@app.route('/runbus/<busnum>/<direction>')
def runbus_status(busnum, direction):
	busnum = busnum + u'路'
	status = Bus.query.filter_by(bus_num=busnum, direction=direction).first().bus
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
	run_bus_url = 'http://wxbus.gzyyjt.net/wei-bus-app/runBus/getByRouteAndDirection/'+route_id+'/0'
	run_bus_res = s.get(run_bus_url, headers=headers)
	runbus = run_bus_res.json()
	return render_template('runbus.html', busnum=busnum, buslist=buslist, runbus=runbus)

if __name__ == '__main__':
	manager.run()