from flask import Blueprint

api = Blueprint("api", __name__)

from . import admin_upload, login_view, view_index, user_detail, pay