# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config



#实例化bootstrap、邮件模块、时间模块、SQL模块
bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
	'''定义应用创建函数'''
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	return app