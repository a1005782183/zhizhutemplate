from config import config_map
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_msearch import Search

import redis

db = SQLAlchemy()
search = Search()

redis_store = None

def create_app(config_name):
    app = Flask(__name__)

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    Session(app)

    search.init_app(app)

    # CSRFProtect(app)

    # 添加自定义转换器
    from zhizhutemplate.utils.commons import ReConverter
    app.url_map.converters['re'] = ReConverter

    # 注册蓝图
    from zhizhutemplate import zzt_app
    app.register_blueprint(zzt_app.api)

    # 注册静态文件蓝图
    from zhizhutemplate import web_static
    app.register_blueprint(web_static.html)

    return app

