from . import api
from flask import jsonify, request, session
from zhizhutemplate.models import User, Upload, Template, Collect
from zhizhutemplate import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
import json

@api.route('/query_all_temp')
def query_all_temp():
    '''获取所有模板分页数据'''
    total = 20  # 显示多少条数据
    page_num = request.args.get('page', 1)
    search = request.args.get('s', '')
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    if search != '' and search != 'index':
        paginate = Template.query.msearch(search, fields=['name', 'content']).paginate(page_num, total, error_out=False)
    else:
        print(2)
        paginate = Template.query.order_by('id').paginate(page_num, total, error_out=False)
    print(search, paginate.items)
    datas = paginate.items
    page = paginate.page  # 当前页数
    pages = paginate.pages  # 总页数
    has_prev = paginate.has_prev  # 是否有上一页
    has_next = paginate.has_next  # 是否有下一页
    prev_num = paginate.prev_num  # 上一页页数
    next_num = paginate.next_num  # 下一页页数
    iter = paginate.iter_pages()  # 页码
    iter_pages = []
    for i in iter:
        iter_pages.append(i)
    # 指定控制页数
    if (pages - page) < 3:  # 如果（总页数-当前页）< 3 就返回最后5个值
        iter_pages = iter_pages[-5:]
    elif page > 3:  # 如果当前页大于3就返回-2 +3
        index = iter_pages.index(page)
        iter_pages = iter_pages[index - 2: index + 3]
    else:
        iter_pages = iter_pages[:5]
    # 把None替换成...
    if None in iter_pages:
        index = iter_pages.index(None)
        iter_pages[index] = "..."
    paginate = {'page': page, 'pages': pages, 'has_prev': has_prev, 'has_next': has_next, 'prev_num': prev_num,
                'next_num': next_num, 'iter_pages': iter_pages}
    data_list = []
    for data in datas:
        data_list.append(data.to_dict())
    return jsonify(data=data_list, paginate=paginate)

@api.route('/detail')
def detail():
    '''查询模板详情'''
    id = request.args.get('id')
    temp = Template.query.filter_by(id=id).first()
    temp.view_num += 1
    db.session.commit()
    return jsonify(data=temp.to_dict())

@api.route('/collect')
def collect():
    '''收藏模板'''
    # 获取用户
    username = session.get('username')
    if username == "":
        return jsonify(errno=0, errmsg='请先登录')
    user = User.query.filter_by(username=username).first()
    tem_id = request.args.get('id')
    user_temp = str(user.id)+str(tem_id)
    tem = Template.query.filter_by(id=tem_id).first()
    coll = Collect(user_id=user.id, template_id=tem_id, user_template=user_temp)
    try:
        db.session.add(coll)
        # 模板收藏次数+1
        tem.collect_num += 1
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        coll = Collect.query.filter_by(user_template=user_temp).first()
        # 模板收藏次数-1
        tem.collect_num -= 1
        db.session.delete(coll)
        db.session.commit()
        # 数据已存在，判断为取消收藏删除数据
        return jsonify(errno=1, errmsg="取消收藏")
    except Exception as e:
        db.session.rollback()
        return jsonify(errno=1, errmsg="查询数据库异常")
    return jsonify(errno=0, errmsg="添加收藏")

@api.route('/query_coll')
def query_coll():
    '''判断用户收藏模板'''
    # 获取用户
    username = session.get('username')
    if username is None:
        return jsonify(errno=0, errmsg='请先登录')
    user = User.query.filter_by(username=username).first()
    coll_list = []
    coll = Collect.query.filter_by(user_id=user.id).all()
    for col in coll:
        coll_list.append(col.template_id)
    return jsonify(errno=0, coll_list=coll_list)

@api.route('/query_not_vip_temp')
def query_not_vip_temp():
    '''获取免费模板分页数据'''
    total = 20  # 显示多少条数据
    page_num = request.args.get('page', 1)
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    paginate = Template.query.order_by('id').paginate(page_num, total, error_out=False)
    datas = paginate.items
    page = paginate.page  # 当前页数
    pages = paginate.pages  # 总页数
    has_prev = paginate.has_prev  # 是否有上一页
    has_next = paginate.has_next  # 是否有下一页
    prev_num = paginate.prev_num  # 上一页页数
    next_num = paginate.next_num  # 下一页页数
    iter = paginate.iter_pages()  # 页码
    iter_pages = []
    for i in iter:
        iter_pages.append(i)
    # 指定控制页数
    if (pages - page) < 3:  # 如果（总页数-当前页）< 3 就返回最后5个值
        iter_pages = iter_pages[-5:]
    elif page > 3:  # 如果当前页大于3就返回-2 +3
        index = iter_pages.index(page)
        iter_pages = iter_pages[index - 2: index + 3]
    else:
        iter_pages = iter_pages[:5]
    # 把None替换成...
    if None in iter_pages:
        index = iter_pages.index(None)
        iter_pages[index] = "..."
    paginate = {'page': page, 'pages': pages, 'has_prev': has_prev, 'has_next': has_next, 'prev_num': prev_num,
                'next_num': next_num, 'iter_pages': iter_pages}
    data_list = []
    for data in datas:
        if data.is_vip == 0:
            data_list.append(data.to_dict())
    return jsonify(data=data_list, paginate=paginate)

@api.route('/query_vip_temp')
def query_vip_temp():
    '''获取VIP模板分页数据'''
    total = 20  # 显示多少条数据
    page_num = request.args.get('page', 1)
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    paginate = Template.query.order_by('id').paginate(page_num, total, error_out=False)
    datas = paginate.items
    page = paginate.page  # 当前页数
    pages = paginate.pages  # 总页数
    has_prev = paginate.has_prev  # 是否有上一页
    has_next = paginate.has_next  # 是否有下一页
    prev_num = paginate.prev_num  # 上一页页数
    next_num = paginate.next_num  # 下一页页数
    iter = paginate.iter_pages()  # 页码
    iter_pages = []
    for i in iter:
        iter_pages.append(i)
    # 指定控制页数
    if (pages - page) < 3:  # 如果（总页数-当前页）< 3 就返回最后5个值
        iter_pages = iter_pages[-5:]
    elif page > 3:  # 如果当前页大于3就返回-2 +3
        index = iter_pages.index(page)
        iter_pages = iter_pages[index - 2: index + 3]
    else:
        iter_pages = iter_pages[:5]
    # 把None替换成...
    if None in iter_pages:
        index = iter_pages.index(None)
        iter_pages[index] = "..."
    paginate = {'page': page, 'pages': pages, 'has_prev': has_prev, 'has_next': has_next, 'prev_num': prev_num,
                'next_num': next_num, 'iter_pages': iter_pages}
    data_list = []
    for data in datas:
        if data.is_vip == 1:
            data_list.append(data.to_dict())
    return jsonify(data=data_list, paginate=paginate)
