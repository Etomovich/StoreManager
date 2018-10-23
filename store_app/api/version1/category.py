from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1 import bp,users,userslist,categories,list_of_categories,products
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


class AllCategories(Resource):
    '''This class implements:

    GET: Which gets a paginated list of all categories'''
    def get(self):
        kur = Kurasa(list_of_categories, 5)
        page = request.args.get('page', 1, type=int)
        category1 = kur.get_items(page)
        category1_details ={}

        for item in category1:
            the_key = item.keys()
            for thing in the_key:
                category1_details[thing]= item[thing]

        reply = {
            "Status": "OK",
            "Categories": category1_details,
            "Total Pages": str(kur.no_of_pages),
            "Next Page":"http://127.0.0.1:5000/api/v1/category?page="+str(page+1) if kur.has_next(page) else "END",
            "Prev Page":"http://127.0.0.1:5000/api/v1/category?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
        }
        answ = make_response(jsonify(reply),200)
        answ.content_type='application/json;charset=utf-8'

        return answ


class CreateCategoryAdmin(Resource):
    '''This class implements:  
    POST: Which creates a new category'''
    @auth.login_required
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
        if 'category_name' not in data or 'category_description' not in data:
            message ='Please ensure that you put in the data for the following keys:[category_name,category_description]'
            return error_response(400,message)

        for item in list_of_categories:
            if item == data['category_name']:
                message ='This category is already in the system'
                return error_response(400,message)

        ##All checks are valid
        list_data= {str(data['category_name']):str(data['category_description'])}
        list_of_categories.append(list_data)

        users[str(data['category_name'])] = str(data['category_description'])

        reply_info = {
            "Status": "CREATED",
            str(data['category_name']):str(data['category_description'])
        }

        answ = make_response(jsonify(reply_info),201)
        answ.content_type='application/json;charset=utf-8'

        return answ

class CategoryDetails(Resource):
    '''This class implements:

    GET: Which gets a specific category   
    PUT: Which edits category details  
    DELETE: Which removes a category. NB:All products in a deleted category will have category value set to none '''
    def get(self, category_name):
        try:
            answer  = {}
            category_details = categories[str(category_name)]
            answer[str(category_name)] = category_details
            ans = make_response(jsonify(answer),200)
            ans.content_type='application/json;charset=utf-8'

            return ans

        except:
            message ='This category does not exist.'
            return error_response(404,message)

    @auth.login_required
    def put(self, category_name):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
        user = data['username']
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            return error_response(403,message)
        try:
            #Check if category is there
            current_category = categories[str(category_name)]

            changes = []

            data = request.get_json(force =True) or {}

            #validate the data
            for key in data.keys():
                if key == "category_name":
                    for item in list_of_categories:
                        cat_name =""
                        for thing in item.keys():
                            cat_name = thing

                        if cat_name == data['category_name']:
                            message ='The category you put is already in the system!!'
                            return error_response(400,message)

                    changes.append("category_name")

                if key == "category_description":
                    changes.append("category_description")

            #Perform changes for valid data
            change_details={}

            if "category_name" in changes and "category_description" in changes:
                changes = []
                changes.append("category_description")
                changes.append("category_name")
        
            for change in changes:
                if change == "category_description":
                    count = 0
                    while count<len(list_of_categories):
                        a_category = list_of_categories[count]

                        cat_name = ""
                        for key in a_category.keys():
                            cat_name = key
                        
                        if cat_name == category_name:
                            list_of_categories[count][cat_name] = data['category_description']
                            change_details["category_description"] = data["category_description"]
                            break                         
                        count = count + 1

                if change == "category_name":
                    cat_details = categories.pop(str(category_name))
                    categories[(data['category_name'])] = cat_details

                    count = 0
                    while count<len(list_of_categories):
                        a_category = list_of_categories[count]

                        cat_name = ""
                        for key in a_category.keys():
                            cat_name = key
                        
                        if cat_name == category_name:
                            cat_description = list_of_categories[count].pop(cat_name)
                            list_of_categories[count][data["category_name"]] = cat_description
                            change_details["category_name"] = data["category_name"]
                            break                         
                        count = count + 1


            reply={"category_changes": change_details,"STATUS":"UPDATED"}
            ans = make_response(jsonify(reply),201)
            ans.content_type='application/json;charset=utf-8'

            return ans              
            

        except:
            message ='This category does not exist.'
            return error_response(404,message)

    @auth.login_required
    def delete(self, category_name):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
        user = data['username']
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            return error_response(403,message)

        try:
            #Check if category is there
            current_category = categories[str(category_name)]

            #pop the category
            deleted_category = categories.pop(str(category_name))

            #remove item in list of categories
            for item in list_of_categories:
                for jina in item.keys():
                    if jina == category_name:
                       list_of_categories.remove(item)  
                    
            answ = make_response(jsonify({"STATUS":"DELETED","Category removed": str(category_name)}),204)
            answ.content_type='application/json;charset=utf-8'

            return answ
        except:
            message ='This category does not exist.'
            return error_response(404,message)

class CategoryProducts(Resource):
    '''This class implements:

    GET: Which gets a paginated list of products in this category'''
    def get(self, category_name):
        try:
            #Check if category is there
            current_category = categories[str(category_name)]
            kur = Kurasa(current_category, 2)
            page = request.args.get('page', 1, type=int)
            cat_items = kur.get_items(page)

            reply = {
                "Items in this Category": cat_items,
                "Total Pages": str(kur.no_of_pages),
                "Next Page":"http://127.0.0.1:5000/api/v1/category/"+str(category_name)+"/products?page="+str(page+1) if kur.has_next(page) else "END",
                "Prev Page":"http://127.0.0.1:5000/api/v1/category/"+str(category_name)+"/products?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
            }
            answ = make_response(jsonify(reply),200)
            answ.content_type='application/json;charset=utf-8'

            return answ


        except:
            message ='This category does not exist.'
            return error_response(404,message)

class SearchCategory(Resource):
    '''This class implements:

    GET: Which gets a paginated list of all products in this category whose name has search_string as a part of it.'''
    def get(self, search_string):
        search_results=[]
        for item in list_of_categories:
            cat_name =""
            for thing in item.keys():
                cat_name = thing
            
            if cat_name.find(search_string) >= 0:
                search_results.append(item)
            
        kur = Kurasa(search_results, 2)
        page = request.args.get('page', 1, type=int)
        cat_selected = kur.get_items(page)


        reply = {
            "Categories": cat_selected,
            "Total Pages": str(kur.no_of_pages),
            "Next Page":"http://127.0.0.1:5000/api/v1/category/search/"+search_string+"?page="+str(page+1) if kur.has_next(page) else "END",
            "Prev Page":"http://127.0.0.1:5000/api/v1/category/search/"+search_string+"?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
        }
        answ = make_response(jsonify(reply),200)
        answ.content_type='application/json;charset=utf-8'

        return answ

the_api.add_resource(AllCategories, "/category")
the_api.add_resource(CategoryDetails, "/admin/category/<category_name>")
the_api.add_resource(CreateCategoryAdmin,"/admin/category")
the_api.add_resource(CategoryProducts, "/category/<category_name>/products")
the_api.add_resource(SearchCategory,"/category/search/<search_string>")