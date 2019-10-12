from zhizhutemplate import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import *
app = create_app("develop")

CORS(app, supports_credentials=True, resources=r'/*') # 允许跨域
app.config['JSON_AS_ASCII'] = False # 设置json编码格式 如果为False 就不使用ascii编码
# app.config['MAX_CONTENT_LENGTH'] = 222 * 1024 * 1024
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
	manager.run()
