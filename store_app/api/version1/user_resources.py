from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1 import bp,users,userslist
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
    

class Start(Resource):
    '''Implements welcome page in Etomovich Stores App'''
    def get(self):
        return ({"message": "Welcome to Etomovich Stores."}, 200)

the_api.add_resource(Start, "/",'/welcome')


class LoginApi(Resource):
    '''Logs in a user into the api. Give  the user a token to perfom transactions as authentication.'''

    def post(self):
        data = request.get_json(force =True) or {}
        if 'username' not in data or 'password' not in data:
            message ='Please ensure that you put in the data for the following keys:[username,password]'
            return error_response(400,message)
        user_name = data['username']
        pass_word = data['password']

        try:
            # confirm that the user does exist
            user = users[data['username']]

            # verify the password
            if check_password_hash(user['password'],pass_word):
                s = Serializer(Config.SECRET_KEY, expires_in=21600)
                token = s.dumps({'username': user_name})
                return({
                'message': 'Login successful!! This token will be used to access all protected endpoints and will be valid for the next 6hrs then you will have to login again to access another token',  
                'Authorization': token.decode('ascii')}, 200)
            else:
                return({'message': 'You have entered a wrong password or username'}, 401)
        except:
            return({'message': 'user does not exist'}, 401)

the_api.add_resource(LoginApi, '/login') 

class UsersCollection(Resource):
    '''This class implements the following admin functions:

    GET: Which gets a paginated list of all users 
    POST: Which creates a new user'''

    @auth.login_required
    def get(self):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        data = s.loads(str(token))
        user = data['username']
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            return error_response(403,message)

        #Return results
        kur = Kurasa(userslist, 2)
        page = request.args.get('page', 1, type=int)
        wangwana = kur.get_items(page)
        wangwana_details ={}

        for item in wangwana:
            wangwana_details[item] = users[item]

        reply = {
            "Status":"OK",
            "Users": wangwana_details,
            "Total Pages": str(kur.no_of_pages),
            "Next Page":"http://127.0.0.1:5000/api/v1/admin/users?page="+str(page+1) if kur.has_next(page) else "END",
            "Prev Page":"http://127.0.0.1:5000/api/v1/admin/users?page="+str(page-1) if kur.has_prev(page) else "BEGINNING"
        }
        answ = make_response(jsonify(reply),200)
        answ.content_type='application/json;charset=utf-8'

        return answ

    @auth.login_required
    def post(self):
        ##Verify user role
        token = request.headers.get('Authorization')
        s = Serializer(Config.SECRET_KEY)
        bank = s.loads(str(token))
        user = bank['username']       
        if users[user]['role'] is not "Admin":
            message ='This is an Admin View!! Contact admin for more details!!'
            #return error_response(403,message)
            return 45

        #Take the data
        data = request.get_json(force =True) or {}
        if 'username' not in data or 'name' not in data or 'email' not in data  or 'phone' not in data  or 'password' not in data or 'retype_password' not in data:
            message ='Please ensure that you put in the data for the following keys:[username,name,email,phone,password,retype_password]'
            #return error_response(4001,message)
            return 1
        
        if data['password'] != data["retype_password"]:
            message ='Make sure password and retype password are equal'
            #return error_response(4002,message)
            return 2


        for pers in userslist:
            if pers == data['username']:
                message ='The username you used is already in the system'
                #return error_response(4003,message)
                return 3

            if users[pers]['email'] == data["email"]:
                message ='The email you used is already in the system'
                #return error_response(4004,message)
                return 4

            if users[pers]['phone'] == data["phone"]:
                message ='The phone number you used is already in the system'
                #return error_response(4005,message)
                return 6

        the_role = "User"
        try:
            if data['role'] == "Admin" or data['role'] == "User":
                the_role= data['role']
            else:
                message ='The role can either be "Admin" or "User"'
                #return error_response(4006,message) 
                return 8
        except:
            the_role='User'

        ##All checks are valid
        userslist.append(str(data['username']))
        person_info = {
            "name": str(data['name']),
            "email": str(data['email']),
            "role": the_role,
            "phone": str(data['phone']),
            "password": generate_password_hash(data["password"])
        }
        users[str(data['username'])] = person_info

        reply_info = {
            "username":str(data['username']),
            "name": str(data['name']),
            "email": str(data['email']),
            "role": the_role,
            "phone": str(data['phone']),
            "STATUS":"CREATED"
        }

        answ = make_response(jsonify(reply_info),201)
        answ.content_type='application/json;charset=utf-8'

        return answ


the_api.add_resource(UsersCollection, "/admin/users")         


