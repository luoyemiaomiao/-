from flask import Blueprint, render_template, request, jsonify, abort
from App.exts import db
from App.models import *
# 创建蓝图
blue = Blueprint('blue', __name__)
def init_blue(app):
    app.register_blueprint(blue)


# 路由和视图函数
@blue.route('/')
def index():
    data = {
        'status':200,
        'msg':'success',
    }
    return jsonify(data)
# 接口 api
# 前后端交互的URL
@blue.route('/user/',methods=['get','post','put','delete'])
def user():
    # get:以获取数据为主，获取用户
    if request.method=='GET':
        page = int(request.args.get('page',1))
        per_page = 5
        p = User.query.paginate(page,per_page,False)
        users = p.items
        # print(users)
        # print(type(users))
        user_dict = []
        for user in users:
            u_dict=user.to_dict()
            user_dict.append(u_dict)
        data = {
            'status': 200,
            'msg': 'success',
            'data':user_dict
        }
        return jsonify(data)
    # post:以提交数据为主，创建用户或更新用户
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data = {
            'status': 200,
            'msg': 'success',
        }
        # 验证客户端提交过来的参数
        if not username or not password:
            data['status'] = 400
            data['msg'] = '用户名或密码错误'
            return jsonify(data)
    #     添加用户
        user = User()
        user.name = username
        user.passwd = password
        try:
            db.session.add(user)
            db.session.commit()
        except:
            data['status'] = 500
            data['msg'] = '创建用户失败'
        return jsonify(data)
    # put:以修改数据为主，更新用户
    elif request.method == 'PUT':
        username = request.form.get('username')
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')
        data = {
            'status': 200,
            'msg': 'success',
        }
        users = User.query.filter(User.name==username,User.passwd==oldpassword)
        if users.count() > 0:
            user = users.first()
            user.passwd = newpassword

            db.session.commit()
        else:
            data['status'] = 400
            data['msg'] = '原密码错误'
            return jsonify(data)
    # delete:以删除数据为主，删除用户
    elif request.method == 'DELETE':
        username = request.form.get('username')
        data = {
            'status': 200,
            'msg': 'success',
        }
        users = User.query.filter(User.name==username)
        if users.count > 0:
            user = users.first()
            db.session.delete(user)
            db.session.commit()
        else:
            data['status'] = 400
            data['msg'] = '用户名不存在'
        return jsonify(data)
    else:
        abort(400)