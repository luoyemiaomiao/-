# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flaskdb2'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 将数据库配置信息拼接
def get_db_uri(dbinfo):
    db = dbinfo.get('DB')
    driver = dbinfo.get('DRIVER')
    user = dbinfo.get('USER')
    password = dbinfo.get('PASSWORD')
    host = dbinfo.get('HOST')
    port = dbinfo.get('PORT')
    name = dbinfo.get('NAME')
    return "{}+{}://{}:{}@{}:{}/{}".format(db, driver, user, password, host, port, name)


class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '110'


# 开发环境
class DevelopConfig(Config):
    DEBUG = True

    # mysql+pymysql://root:root@localhost:3306/flaskdb2
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flaskdb8',
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)



# 测试环境
class TestingConfig(Config):
    TESTING = True

    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flaskdb8',
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


# 生产环境
class ProductConfig(Config):
    DEBUG = False

    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flaskdb8',
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


env = {
    'develop': DevelopConfig,
    'test': TestingConfig,
    'product': ProductConfig,
}