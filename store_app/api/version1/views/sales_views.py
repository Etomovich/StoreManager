from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1.models.products_model import Products
from store_app.api.version1.models.user_model import UserModel
from store_app.api.version1.models.sales_model import Sales
from Instance.config import Config
from store_app.api.version1 import bp


from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from store_app.api.version1.pagination import Kurasa
from store_app.api.version1.errors import error_response

sales_api = Api(bp)

class FetchAllSales(Resource):
    def get(self):
        current_user = ""
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        try:
            data = s.loads(str(token))
            current_user = UserModel.user_fetch_data[data['user_id']]
        except:
            reply="You are not authorized to view this page!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        if current_user['role'] == "User":
            reply="This is an Admin Page contact admin for more help!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        sales_db = Sales()
        reply_info = False
        reply_info = sales_db.list_of_sales()

        if len(reply_info)>0:
            #Return results
            kur = Kurasa(reply_info, 2)
            page = request.args.get('page', 1, type=int)
            wangwana = kur.get_items(page)
            reply = {
                "Status":"OK",
                "Sales": wangwana,
                "Total Pages": str(kur.no_of_pages),
                "Next Page":"http://127.0.0.1:5000/api/v1/sales?page="+str(page+1) if kur.has_next(page) else "END",
                "Prev Page":"http://127.0.0.1:5000/api/v1/sales?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No sale found found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ 

    def post(self):
        current_user = ""
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        try:
            data = s.loads(str(token))
            current_user = UserModel.user_fetch_data[data['user_id']]
        except:
            reply="You are not authorized to view this page!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        if current_user['role'] == "Admin":
            reply="Please create a user account to perform this action!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        data = request.get_json(force =True) or {}
        data['username'] = current_user['username']		 
        sales_db = Sales()
        reply_info = sales_db.create_sale(data)

        if isinstance(reply_info, dict) :
            pack = {"Status":reply_info}
            answ = make_response(jsonify(pack),201)
            answ.content_type='application/json;charset=utf-8'
            return answ
        else:
            pack = {"Status":reply_info}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ      
     

sales_api.add_resource(FetchAllSales, "/sales")

class FetchSpecificSale(Resource):
    def get(self, saleId):
        current_user = ""
        data =False
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        try:
            data = s.loads(str(token))
            current_user = UserModel.user_fetch_data[data['user_id']]
        except:
            reply="You are not authorized to view this page!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        sales_db = Sales()
        reply_info = False
        reply_info = sales_db.get_sale_item(saleId)

        if current_user['role'] == "User" and current_user['username'] != reply_info['attendant']:
            reply="This is an Admin Page contact admin for more help!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        if reply_info:
            #Return results
            reply = {
                "Status":"OK",
                "Product": reply_info,
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No sale found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ
     

sales_api.add_resource(FetchSpecificSale, "/sales/<saleId>")

class SearchSpecificSale(Resource):
    def get(self, name):
        current_user = ""
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        try:
            data = s.loads(str(token))
            current_user = UserModel.user_fetch_data[data['user_id']]
        except:
            reply="You are not authorized to view this page!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        if current_user['role'] == "User":
            reply="This is an Admin Page contact admin for more help!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        sales_db = Sales()
        reply_info = False
        reply_info = sales_db.search_for_sale(name)

        if len(reply_info)>0:
            #Return results
            kur = Kurasa(reply_info, 3)
            page = request.args.get('page', 1, type=int)
            wangwana = kur.get_items(page)
            reply = {
                "Status":"OK",
                "Sales": wangwana,
                "Total Pages": str(kur.no_of_pages),
                "Next Page":"http://127.0.0.1:5000/api/v1/sales/search/<name>?page="+str(page+1) if kur.has_next(page) else "END",
                "Prev Page":"http://127.0.0.1:5000/api/v1/sales/search/<name>?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No sales of this person found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ 

sales_api.add_resource(SearchSpecificSale, "/sales/search/<name>")

class DeleteSale(Resource):
    def delete(self, saleId):
        current_user = ""
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        try:
            data = s.loads(str(token))
            current_user = UserModel.user_fetch_data[data['user_id']]
        except:
            reply="You are not authorized to view this page!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        if current_user['role'] == "Admin":
            reply="Please create a user account to perform this action!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        sales_db = Sales()
        reply_info = False
        reply_info = sales_db.delete_sale_item(saleId)

        if reply_info:
            #Return results
            reply = {
                "Status":"DELETED",
                "Product": saleId,
            }
            answ = make_response(jsonify(reply),204)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No product found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ
             
     

sales_api.add_resource(DeleteSale, "/sales/delete/<saleId>")




