from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1 import bp,users,userslist,categories,list_of_categories,products,list_of_products,items_in_stock,\
                                    recovered_product_ids,list_of_items,recovered_item_ids
                                    
from store_app import create_app

from store_app.api.version1.pagination import Kurasa
from store_app.api.version1.errors import error_response

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from Instance.config import Config
  

from flask_httpauth import HTTPTokenAuth

the_api = Api(bp)


auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False

class AllProducts(Resource):
    '''This class implements:
    GET: Which gets a paginated list of all products
    '''
    @auth.verify_token
    def get(self):
        kur = Kurasa(list_of_products, 2)
        page = request.args.get('page', 1, type=int)
        products_items = kur.get_items(page)


        reply = {
            "Products": products_items,
            "Total Pages": str(kur.no_of_pages),
            "Next Page":"http://127.0.0.1:5000/api/v1/products?page="+str(page+1) if kur.has_next(page) else "END",
            "Prev Page":"http://127.0.0.1:5000/api/v1/products?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
        }
        answ = make_response(jsonify(reply),200)
        answ.content_type='application/json;charset=utf-8'

        return answ

the_api.add_resource(AllProducts, "/products") 

class AdminAllProducts(Resource):
    '''This class implements the following admin functions:

    POST: Which creates a new product. Can only be accessed by admin'''

    @auth.verify_token
    def post(self):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
        user = data['username']
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            return error_response(403,message)

        data = request.get_json(force =True) or {}
        if 'product_name' not in data or 'price' not in data:
            message ='Please ensure that you put in the data for the following keys:[product_name,price,category(optional)]'
            return error_response(400,message)
        

        ##Check data validity
        for item in list_of_products:
            prod_name =""
            jina = item.values()
            for thing in jina:
                prod_name = thing

            if prod_name ==  data['product_name']:
                message ='The product_name already exists!!'
                return error_response(400,message)

        ##All checks are valid. Get an id
        new_product_id = None
        largest_id = 0
        #Check to find largest_id
        if len(list_of_products)>0:
            largest_id = len(list_of_products)
        #Check to see if there are reclaimed ids 
        if len(recovered_product_ids)>0:
            new_product_id = recovered_product_ids[0]
            del recovered_product_ids[0]
        else:
            new_product_id = largest_id + 1

        ##check for product details input
        prod_description_checker = False
        if "product_description" in data.keys():
            prod_description_checker = True

        p_details = {"product_name":data["product_name"],"amount_in_stock": 0,"price":float(data['price']),"product_details": data['product_description'] if prod_description_checker else ""}

        if "category" in data.keys():
            try:
                category_check = categories[data["category"]]
                p_details["category"] = data['category']
            except:
                message ='The category used does not exist!!'
                return error_response(400,message)


        p_item = {"product_details":p_details, "items_in_stock":[]}

        ##Input item 
        products[new_product_id] = p_item
        list_of_products.append({new_product_id:data["product_name"]})
        

        p_details["STATUS"] = "CREATED"

        answ = make_response(jsonify(p_details),201)
        answ.content_type='application/json;charset=utf-8'

        return answ

class ProductsById(Resource):
    '''This class implements:

    GET: Which gets a specific product.'''
    @auth.verify_token
    def get(self, productId):
        try:
            #Check if product is there
            current_product = products[int(productId)]

            answ = make_response(jsonify(current_product),200)
            answ.content_type='application/json;charset=utf-8'

            return answ


        except:
            message ='The requested product does not exist.'
            return error_response(400,message)

class ProductsSearch(Resource):
    '''This class implements:

    GET: Which returns a search of a specific product.'''
    @auth.verify_token
    def get(self, search_string):
        search_results=[]
        for item in list_of_products:
            prod_name =""
            for thing in item.values():
                prod_name = thing
            
            if prod_name.find(search_string) >= 0:
                search_results.append(item)
            
        kur = Kurasa(search_results, 2)
        page = request.args.get('page', 1, type=int)
        cat_selected = kur.get_items(page)


        reply = {
            "Categories": cat_selected,
            "Total Pages": str(kur.no_of_pages),
            "Next Page":"http://127.0.0.1:5000/api/v1/product/search/"+search_string+"?page="+str(page+1) if kur.has_next(page) else "END",
            "Prev Page":"http://127.0.0.1:5000/api/v1/product/search/"+search_string+"?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
        }
        answ = make_response(jsonify(reply),200)
        answ.content_type='application/json;charset=utf-8'

        return answ
    

class AdminProductsById(Resource):
    '''This class implements the following admin functions:
    
    PUT: Which edits a product.  
    DELETE: Which removes a product. Note: Removing a product will remove its associated items'''
    @auth.verify_token
    def put(self, productId):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
        user = data['username']
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            return error_response(403,message)

        try:
            productId = int(productId)
            #Check if user is there
            current_product = products[productId]

            changes = []

            data = request.get_json(force =True) or {}

            #validate the data
            for key in data.keys():
                if key == "product_name":
                    for thing in list_of_products:
                        prod_name = ""
                        name = thing.values()
                        for item_2 in name:
                            prod_name = item_2
                        
                        if prod_name == data["product_name"]:
                            message ='The <product_name> key represents a product already in the system '
                            return error_response(400,message)

                    changes.append("product_name")

                if key == "price":
                    changes.append("price")

                if key == "product_description":
                    changes.append("product_description")

                if key == "category":
                    try:
                        category_check = categories[data["category"]]
                        changes.append("category")
                    except:
                        message ='The category used does not exist!!'
                        return error_response(400,message)

            change_details={}
            for change in changes:
                if change == "product_name":
                    products[productId]["product_details"]["product_name"] = data['product_name']
                    
                    count = 0
                    while count<len(list_of_products):
                        a_prod = list_of_products[count]
                        prod_id = -1
                        pid = a_prod.keys()
                        for thing_1 in pid:
                            prod_id = thing_1

                        if prod_id == productId:
                            list_of_products[count][productId] = data['product_name']
                            change_details['product_name'] = data['product_name']

                        count = count + 1

                if change == "price":
                    products[productId]["product_details"]["price"] = float(data['price'])
                    change_details["price"] = data["price"]

                if change == "category":
                    products[productId]["product_details"]["category"] = data["category"]
                    change_details["category"] = data["category"]

                if change == "product_description":
                    products[productId]["product_details"]["product_description"] = data["product_description"]
                    change_details["product_description"] = data["product_description"]


            reply={"changes_to_product": change_details,"STATUS":"UPDATED"}
            ans = make_response(jsonify(reply),201)
            ans.content_type='application/json;charset=utf-8'

            return ans
            
        except:
            message ='The product you are trying to update does not exist.'
            return error_response(400,message)


    @auth.verify_token
    def delete(self, productId):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
        user = data['username']
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            return error_response(403,message)

        try:
            productId = int(productId)
            #Check if product is there
            current_product = products[productId]

            changes = []

            items_in_product = []
            for item in products["items_in_stock"]:             
                items_in_product.append(item)

            ##Delete all items related to this product
            for thing in items_in_product:
                itemId = thing
                try:
                    itemId = int(itemId)
                    #Try deleting item in item_in_stock dict
                    deleting_item = items_in_stock.pop(itemId)

                    #Remove item in corresponding product
                    products[deleting_item["product_id"]]["items_in_stock"].remove(itemId)

                    #Decrement product amount in stock by one
                    products[deleting_item['']]['product_details']["amount_in_stock"] = products[deleting_item["product_id"]]['product_details']["amount_in_stock"] - 1

                    #Finally Remove item in list of items
                    deletion_item ={"item_id": itemId}
                    list_of_items.remove(deletion_item)
                    recovered_item_ids.append(itemId)

                    #Check for the biggest item id
                    big = -1
                    for it_id in list_of_items:
                        if big<it_id["item_id"]:
                            big = it_id["item_id"]

                    #Use big value to  remove any recovered_item_id that exeeds big
                    for re_id in recovered_item_ids:
                        if re_id>big:
                            recovered_item_ids.remove(re_id)
                
                except:
                    message ='The item you are trying to delete does not exist.'
                    return error_response(400,message)
                
            ##Pop the product out after deleting all items
            product_removed = products.pop(productId)

            answ = make_response(jsonify({"STATUS":"DELETED","Product removed": product_removed}),204)
            answ.content_type='application/json;charset=utf-8'

            return answ
        except:
            message ='The product you are trying to update does not exist.'
            return error_response(400,message)
    


class ProductItemsInStock(Resource):
    '''This class implements:

    GET: Which gets a paginated list of items for this product currently in stock'''
    @auth.verify_token
    def get(self, productId):
        try:
            productId = int(productId)
            #Check if user is there
            current_product_items = products[productId]["items_in_stock"]
            kur = Kurasa(current_product_items, 2)
            page = request.args.get('page', 1, type=int)
            item_ids = kur.get_items(page)
            items_info ={}

            for item in item_ids:
                items_info [item] = items_in_stock[item]

            reply = {
                "Product Items": items_info,
                "Total Pages": str(kur.no_of_pages),
                "Next Page":"http://127.0.0.1:5000/api/v1/product/"+str(productId)+"/items_in_stock?page="+str(page+1) if kur.has_next(page) else "END",
                "Prev Page":"http://127.0.0.1:5000/api/v1/product/"+str(productId)+"/items_in_stock?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'

            return answ

        except:
            message ='The product you are trying to access does not exist.'
            return error_response(400,message)




the_api.add_resource(AdminAllProducts, "/admin/products")
the_api.add_resource(ProductsById, "/product/<productId>")
the_api.add_resource(ProductsSearch,"/product/search/<search_string>")
the_api.add_resource(AdminProductsById, "/admin/product/<productId>")
the_api.add_resource(ProductItemsInStock,"/product/<productId>/items_in_stock")

