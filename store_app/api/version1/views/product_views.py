from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1.models.products_model import Products
from store_app.api.version1.models.user_model import UserModel
from store_app import create_app
from Instance.config import Config
from store_app.api.version1 import bp

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from store_app.api.version1.pagination import Kurasa
from store_app.api.version1.errors import error_response

from flask_httpauth import HTTPTokenAuth

products_api = Api(bp)

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        data = s.loads(str(token))
    except:
        return False
    if 'user_id' in data:
        g.user = data['user_id']
        return True
    return False

@auth.verify_token
class FetchAllProducts(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        user_id = s.loads(str(token))
        try:
            this_user = UserModel.user_fetch_data[user_id]
        except:
            reply_info = "UNKNOWN USER!!"
            answ = make_response(jsonify(reply_info),201)
            answ.content_type='application/json;charset=utf-8'
            return answ

        #Return results
        prod = Products()
        kur = Kurasa(prod.list_of_products, 3)
        page = request.args.get('page', 1, type=int)
        pag_prod = kur.get_items(page)
        prod_details ={}

        count=1
        for item in pag_prod:
            prod_details[count] = prod.get_product_item(item)
            count = count +1
            
        reply = {
            "Status":"OK",
            "Products": prod_details,
            "Total Pages": str(kur.no_of_pages),
            "Next Page":"http://127.0.0.1:5000/api/v1/products?page="+str(page+1) if kur.has_next(page) else "END",
            "Prev Page":"http://127.0.0.1:5000/api/v1/products?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
        }
        answ = make_response(jsonify(reply),200)
        answ.content_type='application/json;charset=utf-8'        
     

products_api.add_resource(FetchAllProducts, "/products")


@auth.verify_token
class FetchSpecificProduct(Resource):
    def get(self, productId):
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        user_id = s.loads(str(token))
        try:
            this_user = UserModel.user_fetch_data[user_id]
        except:
            reply_info = "UNKNOWN USER!!"
            answ = make_response(jsonify(reply_info),201)
            answ.content_type='application/json;charset=utf-8'
            return answ

        #Return results
        prod = Products()
        prod_details = prod.get_product_item(int(productId))

        if prod_details:           
            reply = {
                "Status":"OK",
                "Products": prod_details
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'
        else:
            reply = {
                "Status":"FAILED",
                "Message": "Product cannot be found!!"
            }
            answ = make_response(jsonify(reply),400)
            answ.content_type='application/json;charset=utf-8'
     

products_api.add_resource(FetchSpecificProduct, "/products/<productId>")
