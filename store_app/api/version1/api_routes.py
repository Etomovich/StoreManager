from flask import request, make_response, jsonify,g
from flask_restful import Resource, Api
from store_app.api.version1 import bp

from store_app.api.version1.pagination import Kurasa
from store_app.api.version1.errors import error_response

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from Instance.config import Config

from flask_httpauth import HTTPTokenAuth

the_api = Api(bp)


def verify_authentication_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user = data['username']
    return user

auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):
    # Authenticating the token
    user = verify_authentication_token(token)
    if not user:
        return False
    g.user = user
    return True


users = {
     "etomovich":
                {
                    "name":"James Etole",
                    "email":"etolejames@gmail.com",
                    "role":"admin",
                    "phone":"0717823158",
                    "password":'pbkdf2:sha256:50000$0cqd8PAJ$cf9e33813d77fae6939eca1219d87296ab59e793c0249b7b0267ab2bd0f8d3d8'  
                }
}## Stores the users

class Start(Resource):
    '''Implements welcome page in Etomovich Stores App'''
    def get(self):
        return ({"message": "Welcome to Etomovich Stores."}, 200)

the_api.add_resource(Start, "/",'/welcome')

class ProtectedResource(Resource):
    '''Implements welcome page in Etomovich Stores App'''
    @auth.login_required
    def get(self):
        return ({"message": "Protected resource."}, 200)

the_api.add_resource(ProtectedResource, '/protected')


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
            if check_password_hash(user['password'],user_name):
                s = Serializer(Config.SECRET_KEY, expires_in=60000)
                token = s.dumps({'username': user_name})
                return({'message': 'login successful',  'Authorization': token.decode('ascii')}, 200)
            else:
                return({'message': 'You have entered a wrong password or username'}, 401)
        except:
            return({'message': 'user does not exist'}, 404)

the_api.add_resource(LoginApi, '/login')        
            


