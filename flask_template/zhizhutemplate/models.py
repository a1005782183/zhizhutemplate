from zhizhutemplate import db

class User(db.Model):
    """用户表"""
    __tablename__ = "zzt_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False) # 账号
    password = db.Column(db.String(256), nullable=False) # 密码
    is_vip = db.Column(db.Integer, default=0) # 是否vip
    download_id = db.relationship("Download") # 下载id
    collect_id = db.relationship("Collect")  # 收藏id
    template_id = db.relationship("Template")  # 模板id

    def to_dict(self):
        data_dict = {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'is_vip': self.is_vip,
        }
        return data_dict


class Template(db.Model):
    '''模板表'''
    __tablename__  = "zzt_template"
    __searchable__ = ['name', 'content']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) # 名称
    content = db.Column(db.String(255), nullable=True) # 内容
    view_num = db.Column(db.Integer, default=0) # 观看次数
    is_vip = db.Column(db.Integer, default=0)  # 是否vip
    collect_num = db.Column(db.Integer, default=0) # 收藏次数
    down_num = db.Column(db.Integer, default=0) # 下载次数
    img = db.Column(db.String(255), nullable=False) # 图片
    file_name = db.Column(db.String(255), nullable=False) # 上传文件的文件名
    file_type = db.Column(db.String(255), nullable=True)  # 文件类型
    user_id = db.Column(db.ForeignKey("zzt_user.id"), nullable=False, default=1)  # 用户id

    def to_dict(self):
        data_dict = {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'view_num': self.view_num,
            'is_vip': self.is_vip,
            'collect_num': self.collect_num,
            'down_num': self.down_num,
            'img': self.img,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'user_id': self.user_id
        }
        username = User.query.filter_by(id=self.user_id).first()
        data_dict['username'] = username.username
        return data_dict


class Download(db.Model):
    '''下载表'''
    __tablename__ = "zzt_download"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("zzt_user.id"), nullable=False) # 用户id
    template_id = db.Column(db.ForeignKey("zzt_template.id"), nullable=False) # 模板id
    user_template = db.Column(db.String(255), unique=True, nullable=False)  # 判断是否存在


class Upload(db.Model):
    '''上传表'''
    __tablename__  = "zzt_upload"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) # 名称
    content = db.Column(db.String(255), nullable=True) # 内容
    down_type = db.Column(db.Integer, default=0) # 下载类型
    img = db.Column(db.String(255), nullable=False) # 图片
    file_name = db.Column(db.String(255), unique=True, nullable=False) # 上传文件的文件名
    file_type = db.Column(db.String(255), nullable=True)  # 文件类型
    user_id = db.Column(db.ForeignKey("zzt_user.id"), nullable=False, default=1)  # 用户id

    def to_dict(self):
        data_dict = {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'down_type': self.down_type,
            'img': self.img,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'user_id': self.user_id
        }
        username = User.query.filter_by(id=self.user_id).first()
        data_dict['username'] = username.username
        return data_dict

class Collect(db.Model):
    '''收藏表'''
    __tablename__ = "zzt_collect"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("zzt_user.id"), nullable=False) # 用户id
    template_id = db.Column(db.ForeignKey("zzt_template.id"), nullable=False) # 模板id
    user_template = db.Column(db.String(255), unique=True, nullable=False) # 判断是否存在


