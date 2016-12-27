# -*- coding: utf-8 -*-
from . import db
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