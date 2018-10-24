from flask import request, make_response, jsonify

from flask_restful import Resource, Api
from store_app.api.version1 import bp, user_model
from store_app.api.version1.errors import error_response

user_api = Api(bp)

class UserViews(Resource):
    def post(self):
        try:
            auth= False
            auth = request.headers['Authorization']
        except:
            reply_info = "This is a protected View!! Provide you login token!!"
            answ = make_response(jsonify(reply_info),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        data = request.get_json(force =True) or {}
        if auth:
            data['Authorization'] = auth 
        user_db = user_model.UserModel()
        reply_info = user_db.create_user(data)

        answ = make_response(jsonify(reply_info),201)
        answ.content_type='application/json;charset=utf-8'

        return answ


user_api.add_resource(UserViews, "/register")