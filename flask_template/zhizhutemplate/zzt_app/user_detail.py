from . import api
from flask import jsonify, request, session
from zhizhutemplate.models import User, Upload, Template, Collect, Download
from zhizhutemplate import db
from sqlalchemy.exc import IntegrityError

@api.route('/user_detail_collect')
def user_detail_collect():
    '''获取用户收藏的模板'''
    username = session.get('username')
    if username is None:
        return jsonify(errno=0, errmsg="用户未登录")
    user = User.query.filter_by(username=username).first()
    coll = Collect.query.filter_by(user_id=user.id).all()
    data = []
    for c in coll:
        temp = Template.query.filter_by(id=c.template_id).first()
        data.append(temp.to_dict())
    return jsonify(errno=0, data=data)

@api.route('/user_detail_upload')
def user_detail_upload():
    '''查询用户上传的模板'''
    username = session.get('username')
    if username is None:
        return jsonify(errno=0, errmsg="用户未登录")
    user = User.query.filter_by(username=username).first()
    data = []
    for temp in user.template_id:
        data.append(temp.to_dict())
    return jsonify(errno=0, data=data)

@api.route('/user_detail_down')
def user_detail_down():
    '''查询用户下载的模板'''
    username = session.get('username')
    if username is None:
        return jsonify(errno=0, errmsg="用户未登录")
    user = User.query.filter_by(username=username).first()
    down = Download.query.filter_by(user_id=user.id).all()
    data = []
    for d in down:
        temp = Template.query.filter_by(id=d.template_id).first()
        data.append(temp.to_dict())
    return jsonify(errno=0, data=data)