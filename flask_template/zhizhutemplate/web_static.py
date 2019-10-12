from flask_wtf import csrf
from flask import Blueprint, current_app, make_response

# 提供静态文件的蓝图
html = Blueprint("web_static", __name__)

@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """提供html静态文件"""

    html_file_name = "static_templates/" + html_file_name
    resp = make_response(current_app.send_static_file(html_file_name))
    return resp