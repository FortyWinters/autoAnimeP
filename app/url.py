# 接口url地址定义

from flask import Blueprint
from flask_restful import Api
from app.test.api import Test

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# 注册路由
api.add_resource(Test, '/test')