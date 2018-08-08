from App.exts import db
from App.models import *
from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request

class Hello(Resource):
    def get(self):
        return {'msg':'GET请求'}
    def post(self):
        return {'msg':'POST请求'}

# 定义格式化字段
users_fields = {
    "msg":fields.String,
    'data':fields.String(attribute='private_data'),
    'status':fields.Integer(default=200),
}
#
class Users(Resource):
    # 给get使用格式化字段
    @marshal_with(users_fields)
    def get(self):
        # users = User.query.all()
        # return {'data':users}
        data ={
            'msg':'获取成功',
            'data':'用户数据',
            'code': '404',
            'private_data':'私有属性',
        }
        return  data
#
usermodel_fields ={
    'id':fields.Integer,
    'name':fields.String,
    # 'passwd':fields.String,
    'url':fields.Url('id',absolute=True)#反向解析
}
user2_field = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.Nested(usermodel_fields)
}
# 字典套字典
class User2(Resource):
    @marshal_with(user2_field)
    def get(self):
        user = User.query.first()
        data = {
            'status':200,
            'msg':'ok',
            'data':user
        }
        return data

#
users3_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.List(fields.Nested(usermodel_fields))
}
#字典包含列表
class User3(Resource):
    # 装饰器
    @marshal_with(users3_fields)
    def get(self):
        users = User.query.all()
        data = {
            'status':200,
            'msg':'ok',
            'data':users
        }
        return data

# 请求参数解析
parser = reqparse.RequestParser()
parser.add_argument('name',type=str,required=True,help="name必须传")
parser.add_argument('id',type=int)
parser.add_argument('likes',type=str,action='append')
class Users4(Resource):
    def get(self):
        # name = request.args.get('name')
        # 解析参数对象
        parse = parser.parse_args()
        name = parse.get('name')
        id = parse.get('id')
        likes = parse.get('likes')
        return {'name':name,'id':id,'likes':likes}