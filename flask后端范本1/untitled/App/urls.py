from App.apis import *
from App.exts import api

# /路由
api.add_resource(Hello,'/')
api.add_resource(Users,'/users/')
api.add_resource(User2,'/users2/',endpoint='id')
api.add_resource(User3,'/users3/')
api.add_resource(Users4,'/users4/')