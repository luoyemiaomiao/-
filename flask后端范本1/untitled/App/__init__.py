from flask import Flask
from App.exts import init_exts
from App.settings import env
from App.urls import *

def create_app(envinfo='develop'):
    app = Flask(__name__)

    # 加载项目配置信息
    app.config.from_object(env.get(envinfo))

    # 初始化第三方插件
    init_exts(app)


    return app