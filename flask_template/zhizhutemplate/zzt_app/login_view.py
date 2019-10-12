from . import api
from flask import jsonify, request, session
from zhizhutemplate.models import User
from zhizhutemplate import db
from sqlalchemy.exc import IntegrityError
import json


@api.route('/login', methods=['POST'])
def login():
    '''登录'''
    # 获取数据
    data = request.get_data().decode('utf-8')
    # JSON转为字典
    data = json.loads(data)
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return jsonify(errno=1, errmsg='数据不完整')
    try:
        user = User.query.filter_by(username=username, password=password).first()
    except Exception as e:
        return jsonify(errno=1, errmsg="查询数据错误")
    if user is None:
        return jsonify(errno=1, errmsg="用户名或密码错误")
    session['username'] = username
    return jsonify(errno=0, errmsg="登录成功!", username=username)

@api.route('/register', methods=['POST'])
def register():
    '''注册'''
    # 获取数据
    data = request.get_data().decode('utf-8')
    # JSON转为字典
    data = json.loads(data)
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return jsonify(errno=1, errmsg='数据不完整')
    user = User(username=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        return jsonify(errno=1, errmsg="用户已存在")
    except Exception as e:
        db.session.rollback()
        return jsonify(errno=1, errmsg="查询数据库异常")

    return jsonify(errno=0, errmsg="注册成功")

@api.route('/get_session')
def get_session():
    '''查询用户登录缓存'''
    username = session.get("username")
    if username is None:
        return jsonify(errno=1)
    user = User.query.filter_by(username=username).first()
    return jsonify(errno=0, username=username, is_vip=user.is_vip)

@api.route('/get_user_vip')
def get_user_vip():
    '''获取用户是否vip信息'''
    username = session.get("username")
    if username is None:
        return jsonify(errno=1, errmsg="用户未登录")
    user = User.query.filter_by(username=username).first()
    return jsonify(errno=0, user_vip=user.is_vip)

@api.route("/del_session")
def del_session():
    '''退出用户'''
    session.pop('username')
    return jsonify(errmsg="退出用户")
