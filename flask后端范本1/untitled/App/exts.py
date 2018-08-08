# 在这里导入和初始化第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
# 创建对象
db = SQLAlchemy()
migrate = Migrate()
api = Api()

# 初始化第三方插件
def init_exts(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    api.init_app(app)