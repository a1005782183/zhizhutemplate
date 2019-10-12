from . import api
from flask import jsonify, request, session
from zhizhutemplate.models import User, Upload, Template, Download
from zhizhutemplate import db
from sqlalchemy.exc import IntegrityError
import json
import re

import os

@api.route("/upload_file", methods=['POST'])
def upload_file():
    '''接收文件并保存到数据库文件表'''
    # 获取用户
    username = session.get("username")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(errmsg='请登录用户！')
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 获取文件数据
    file = request.files.get('fileField')
    fileImg = request.files.get('fileImg')
    title = request.form.get('title')
    content = request.form.get('content')
    is_vip = request.form.get('is_vip')
    # 判断数据是否完整
    if all([file, fileImg, title, content, is_vip]):
        # 验证文件格式
        types = ['rar', '7z', 'zip']
        filename = ''.join(re.findall(r'(.*?).zip|(.*?).7z|(.*?).rar', file.filename)[0])
        file_type = "."+str(file.filename).split('.')[-1]
        if file.filename.split('.')[-1] in types:
            # 判断是否有文件夹，没有创建
            path = BASE_DIR+'\\static\\static_templates\\' + filename
            if not os.path.exists(path):
                os.makedirs(path)
                # 保存文件
                file.save(os.path.join(path, file.filename))
                # 保存图片
                imgTypes = ['png', 'jpg']
                if fileImg.filename.split('.')[-1] in imgTypes:
                    fileImg.save(os.path.join(path, fileImg.filename))
                    # 保存数据到数据库
                    files = Upload(name=title, content=content, down_type=is_vip, img=fileImg.filename, file_name=filename, file_type=file_type, user_id=user.id)
                    try:
                        db.session.add(files)
                        db.session.commit()
                    except IntegrityError as e:
                        # 数据库操作错误后的回滚
                        db.session.rollback()
                        return jsonify(errmsg="文件已存在")
                    except Exception as e:
                        db.session.rollback()
                        return jsonify(errmsg="查询数据库异常")
                    return jsonify(errmsg="上传成功！")
            return jsonify(errmsg="文件名重复！")
        return jsonify(errmsg="上传文件格式错误！")
    return jsonify(errmsg="数据不完整！")

@api.route('/query_file')
def query_file():
    '''查询文件表'''
    total = 5  # 显示多少条数据
    page_num = request.args.get('page', 1)
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    # 获取所有文件数据
    paginate = Upload.query.order_by('id').paginate(page_num, total, error_out=False)
    datas = paginate.items
    page = paginate.page # 当前页数
    pages = paginate.pages # 总页数
    has_prev = paginate.has_prev # 是否有上一页
    has_next = paginate.has_next # 是否有下一页
    prev_num = paginate.prev_num # 上一页页数
    next_num = paginate.next_num # 下一页页数
    iter = paginate.iter_pages() # 页码
    iter_pages = []
    for i in iter:
        iter_pages.append(i)
    # 指定控制页数
    if (pages - page) < 3: # 如果（总页数-当前页）< 3 就返回最后5个值
        iter_pages = iter_pages[-5:]
    elif page > 3: # 如果当前页大于3就返回-2 +3
        index = iter_pages.index(page)
        iter_pages = iter_pages[index-2: index+3]
    else:
        iter_pages = iter_pages[:5]
    # 把None替换成...
    if None in iter_pages:
        index = iter_pages.index(None)
        iter_pages[index] = "..."
    paginate = {'page':page, 'pages':pages, 'has_prev':has_prev, 'has_next':has_next, 'prev_num':prev_num, 'next_num':next_num, 'iter_pages':iter_pages}
    data_list = []
    for data in datas:
        data_list.append(data.to_dict())
    return jsonify(data=data_list, paginate=paginate)

@api.route('/agree_file', methods=['POST'])
def agree_file():
    '''同意上传文件到模板里'''
    # 获取数据
    data = request.get_data().decode('utf-8')
    data = json.loads(data)[0]
    # 保存数据到数据库
    temp = Template(name=data['name'],content=data['content'],is_vip=data['down_type'],img=data['img'],file_name=data['file_name'],file_type=data['file_type'], user_id=data['user_id'])
    # 查询上传表数据并删除
    upload = Upload.query.filter_by(id=data['id']).first()
    try:
        db.session.add(temp)
        db.session.delete(upload)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        return jsonify(errmsg="保存失败")
    except Exception as e:
        db.session.rollback()
        return jsonify(errmsg="查询数据库异常")
    return jsonify(errmsg="保存成功")

@api.route('/no_agree_file', methods=['POST'])
def no_agree_file():
    '''不同意上传文件到模板里'''
    # 获取数据
    data = request.get_data().decode('utf-8')
    data = json.loads(data)[0]
    # 查询上传表数据并删除
    upload = Upload.query.filter_by(id=data['id']).first()
    try:
        db.session.delete(upload)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        return jsonify(errmsg="删除失败")
    except Exception as e:
        db.session.rollback()
        return jsonify(errmsg="查询数据库异常")
    return jsonify(errmsg="删除成功")

@api.route('/query_template')
def query_template():
    '''获取模板分页数据'''
    total = 5 # 显示多少条数据
    page_num = request.args.get('page', 1)
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    paginate = Template.query.order_by('id').paginate(page_num, total, error_out=False)
    datas = paginate.items
    page = paginate.page # 当前页数
    pages = paginate.pages # 总页数
    has_prev = paginate.has_prev # 是否有上一页
    has_next = paginate.has_next # 是否有下一页
    prev_num = paginate.prev_num # 上一页页数
    next_num = paginate.next_num # 下一页页数
    iter = paginate.iter_pages() # 页码
    iter_pages = []
    for i in iter:
        iter_pages.append(i)
    # 指定控制页数
    if (pages - page) < 3: # 如果（总页数-当前页）< 3 就返回最后5个值
        iter_pages = iter_pages[-5:]
    elif page > 3: # 如果当前页大于3就返回-2 +3
        index = iter_pages.index(page)
        iter_pages = iter_pages[index-2: index+3]
    else:
        iter_pages = iter_pages[:5]
    # 把None替换成...
    if None in iter_pages:
        index = iter_pages.index(None)
        iter_pages[index] = "..."
    paginate = {'page':page, 'pages':pages, 'has_prev':has_prev, 'has_next':has_next, 'prev_num':prev_num, 'next_num':next_num, 'iter_pages':iter_pages}
    data_list = []
    for data in datas:
        data_list.append(data.to_dict())
    return jsonify(data=data_list, paginate=paginate)

@api.route("/modify", methods=["POST"])
def modify():
    '''修改模板内容'''
    data = request.get_data().decode('utf-8')
    data = json.loads(data)
    temp = Template.query.filter_by(id=data['id']).first()
    temp.name = data['name']
    temp.content = data['content']
    temp.view_num = data['view_num']
    temp.is_vip = data['is_vip']
    temp.down_num = data['down_num']
    temp.img = data['img']
    temp.file_name = data['file_name']
    try:
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        return jsonify(errmsg="保存失败")
    except Exception as e:
        db.session.rollback()
        return jsonify(errmsg="数据库异常")
    return jsonify(errmsg="修改成功")

@api.route('/query_user')
def query_user():
    '''获取用户分页数据'''
    total = 5 # 显示多少条数据
    page_num = request.args.get('page', 1)
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    paginate = User.query.order_by('id').paginate(page_num, total, error_out=False)
    datas = paginate.items
    page = paginate.page # 当前页数
    pages = paginate.pages # 总页数
    has_prev = paginate.has_prev # 是否有上一页
    has_next = paginate.has_next # 是否有下一页
    prev_num = paginate.prev_num # 上一页页数
    next_num = paginate.next_num # 下一页页数
    iter = paginate.iter_pages() # 页码
    iter_pages = []
    for i in iter:
        iter_pages.append(i)
    # 指定控制页数
    if (pages - page) < 3: # 如果（总页数-当前页）< 3 就返回最后5个值
        iter_pages = iter_pages[-5:]
    elif page > 3: # 如果当前页大于3就返回-2 +3
        index = iter_pages.index(page)
        iter_pages = iter_pages[index-2: index+3]
    else:
        iter_pages = iter_pages[:5]
    # 把None替换成...
    if None in iter_pages:
        index = iter_pages.index(None)
        iter_pages[index] = "..."
    paginate = {'page':page, 'pages':pages, 'has_prev':has_prev, 'has_next':has_next, 'prev_num':prev_num, 'next_num':next_num, 'iter_pages':iter_pages}
    data_list = []
    for data in datas:
        data_list.append(data.to_dict())
    print(data_list)
    return jsonify(data=data_list, paginate=paginate)

@api.route("/user_modify", methods=["POST"])
def user_modify():
    '''修改用户内容'''
    data = request.get_data().decode('utf-8')
    data = json.loads(data)
    user = User.query.filter_by(id=data['id']).first()
    user.username = data['username']
    user.password = data['password']
    user.is_vip = data['is_vip']
    try:
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        return jsonify(errmsg="保存失败")
    except Exception as e:
        db.session.rollback()
        return jsonify(errmsg="数据库异常")
    return jsonify(errmsg="修改成功")

@api.route('/add_down_num')
def add_down_num():
    '''添加下载次数'''
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    id = request.args.get('id')
    temp = Template.query.filter_by(id=id).first()
    temp.down_num += 1
    user_template = str(user.id)+str(temp.id)
    down = Download(user_id=user.id, template_id=temp.id, user_template=user_template)
    try:
        db.session.add(down)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        return jsonify(errno=0, errmsg="用户下载过")
    except Exception as e:
        db.session.rollback()
        return jsonify(errno=1, errmsg="数据库异常")
    return jsonify(errno=0, errmsg="下载成功")