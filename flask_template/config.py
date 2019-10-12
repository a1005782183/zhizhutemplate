import redis
import mysql.connector

class Config():
	'''配置文件'''
	DEBUG = True

	SECRET_KEY = "zhizhutemplate"

	# 数据库
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:a5856525400@127.0.0.1:4445/zhizhutemplate"
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	# redis
	REDIS_HOST = "127.0.0.1"
	REDIS_PORT = 6379

	# flask-session配置
	SESSION_TYPE = "redis"
	SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
	SESSION_USE_SIGNER = True
	PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
	"""开发环境"""
	DEBUG = True


class ProductionConfig(Config):
	"""生产环境"""
	pass

config_map = {
	"develop": DevelopmentConfig,
	"product": ProductionConfig
}