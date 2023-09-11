# 编写接口文件

from flask_restful import request, Resource, reqparse, abort
from flask_jwt_extended import jwt_required
from flask import current_app
from lib import common

class Test(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('start', type=int, default=0, location='json')
        self.reqparse.add_argument('length', type=int, default=50, location='json')
        self.reqparse.add_argument('time', type=str, default="", location='json')
        super(Test, self).__init__()

    @jwt_required
    def get(self):
        id = request.args.get('id')
        print(id)
        current_app.logger.error(id)
        return common.trueReturn('', '成功接收到数据')

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        return common.trueReturn('', '成功接收到数据')