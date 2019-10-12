from . import api
from flask import jsonify, session, request
from zhizhutemplate.models import User
from zhizhutemplate import db
from alipay import AliPay
import os
import json

@api.route('/add_vip')
def add_vip():
    '''加入vip'''
    username = session.get("username")
    if username is None:
        return jsonify(errno=1, errmsg="用户未登录")
    user = User.query.filter_by(username=username).first()
    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016100100637110",  # 设置签约的appid
        app_notify_url=None,  # 异步支付通知url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),  # 设置应用私钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/app_public_key.pem"),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2", # RSA 或者 RSA2
        debug=True,  # 默认False,            # 设置是否是沙箱环境，True是沙箱环境
    )

    order_string = alipay_client.api_alipay_trade_page_pay(
        # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
        out_trade_no= user.id,  # 订单号
        total_amount="200",  # 支付金额
        subject="蜘蛛模板",  # 订单名称
        return_url="http://localhost:8080/#/success_vip",  # 支付成功后，跳转url 【客户端显示】
        notify_url=None,
    )
    # 构建让用户跳转的支付宝链接地址
    pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return jsonify(errno=0, errmsg="跳转成功", data=pay_url)

@api.route('/success_vip', methods=["POST"])
def success_vip():
    '''vip充值成功'''

    username = session.get("username")
    user = User.query.filter_by(username=username).first()

    # alipay_dict = request.get_data().decode("utf-8")
    # alipay_dict = json.loads(alipay_dict)
    # alipay_sign = alipay_dict.pop('sign')
    #
    # print(alipay_dict)
    # print(alipay_sign)
    #
    # # 创建支付宝sdk的工具对象
    # alipay_client = AliPay(
    #     appid="2016100100637110",  # 设置签约的appid
    #     app_notify_url=None,  # 异步支付通知url
    #     app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),  # 设置应用私钥
    #     alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/app_public_key.pem"),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #     sign_type="RSA2", # RSA 或者 RSA2
    #     debug=True,  # 默认False,            # 设置是否是沙箱环境，True是沙箱环境
    # )
    # # 借助工具验证参数的合法性
    # # 如果确定参数是支付宝的，返回True，否则返回false
    # result = alipay_client.verify(alipay_dict, alipay_sign)
    # print(result)
    # if result:
    try:
        user.is_vip = 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return jsonify(error=0, errmsg="充值成功")

