# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from wtforms import ValidationError
from ..models import Bus
class BusNum(Form):
	num = StringField(u'公交路数', validators=[Required()])
	submit = SubmitField(u'查询')

	def validate_num(self, filed):
		if not Bus.query.filter_by(bus_num= filed.data.upper() + u'路').first():
			raise ValidationError(u'无此公交线路')

