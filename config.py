# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
	'sqlite:///' + os.path.join(basedir,'businfo-dev.db')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
	'sqlite:///' + os.path.join(basedir,'businfo.db')

config = {
	'development': DevelopmentConfig,
	'production' : ProductionConfig,
	'default': DevelopmentConfig
}
