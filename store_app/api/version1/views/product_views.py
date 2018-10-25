from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1.models.products_model import Products
from store_app.api.version1.models.user_model import UserModel
from Instance.config import Config
from store_app.api.version1 import bp

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from store_app.api.version1.pagination import Kurasa
from store_app.api.version1.errors import error_response

products_api = Api(bp)




class FetchAllProducts(Resource):
    def get(self):
        product_db = Products()
        reply_info = False
        reply_info = product_db.list_of_products()

        if len(reply_info)>0:
            #Return results
            kur = Kurasa(reply_info, 2)
            page = request.args.get('page', 1, type=int)
            wangwana = kur.get_items(page)
            reply = {
                "Status":"OK",
                "Products": wangwana,
                "Total Pages": str(kur.no_of_pages),
                "Next Page":"http://127.0.0.1:5000/api/v1/products?page="+str(page+1) if kur.has_next(page) else "END",
                "Prev Page":"http://127.0.0.1:5000/api/v1/products?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No product found!!"}
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

        if current_user['role'] == "User":
            reply="This is an Admin Page contact admin for more help!!"
            answ = make_response(jsonify(reply),401)
            answ.content_type='application/json;charset=utf-8'
            return answ

        data = request.get_json(force =True) or {}		 
        product_db = Products()
        reply_info = product_db.create_product(data)

        if reply_info == "CREATED":
            pack = {"Status":reply_info}
            answ = make_response(jsonify(pack),201)
            answ.content_type='application/json;charset=utf-8'
            return answ
        else:
            pack = {"Status":reply_info}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ      
     

products_api.add_resource(FetchAllProducts, "/products")



class FetchSpecificProduct(Resource):
    def get(self, productId):
        product_db = Products()
        reply_info = False
        reply_info = product_db.get_product_item(productId)

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
            pack = {"Status":"No product found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ
     

products_api.add_resource(FetchSpecificProduct, "/products/<productId>")

class SearchSpecificProduct(Resource):
    def get(self, name):
        product_db = Products()
        reply_info = False
        reply_info = product_db.search_for_product(name)

        if len(reply_info)>0:
            #Return results
            kur = Kurasa(reply_info, 2)
            page = request.args.get('page', 1, type=int)
            wangwana = kur.get_items(page)
            reply = {
                "Status":"OK",
                "Products": wangwana,
                "Total Pages": str(kur.no_of_pages),
                "Next Page":"http://127.0.0.1:5000/api/v1/products/search/<name>?page="+str(page+1) if kur.has_next(page) else "END",
                "Prev Page":"http://127.0.0.1:5000/api/v1/products/search/<name>?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No product found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ 

products_api.add_resource(SearchSpecificProduct, "/products/search/<name>")

class DeleteProduct(Resource):
    def delete(self, productId):
        product_db = Products()
        reply_info = False
        reply_info = product_db.delete_item(productId)

        if reply_info:
            #Return results
            reply = {
                "Status":"DELETED",
                "Product": productId,
            }
            answ = make_response(jsonify(reply),204)
            answ.content_type='application/json;charset=utf-8'
            return answ 
        else:
            pack = {"Status":"No product found!!"}
            answ = make_response(jsonify(pack),400)
            answ.content_type='application/json;charset=utf-8'
            return answ
             
     

products_api.add_resource(DeleteProduct, "/products/delete/<productId>")



    
     


