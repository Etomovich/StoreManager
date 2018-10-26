import uuid
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

from Instance.config import Config

class UserModel(object):
    '''This class allows a user to implement CRUD on a user object 
    '''
    user_fetch_data={}

    def create_user(self, data={}):
        '''This method allows the admin to create a user'''

        #Data validation
        if 'username' not in data or 'name' not in data or 'email' not in data  or 'phone' not\
                                                in data  or 'password' not in data or 'retype_password' not in data:
            message ='Incomplete data!!'
            return message
        for key in data.keys():
            #Check email validation
            if key == 'email':
                if data[key].find("@") < 2:
                    message ='Incorrect email format'
                    return message

            if key == 'password':
                if data['password'] != data["retype_password"]:
                    message ='Retype password and password should be equal.'
                    return message

            if key == 'role':
                if data['role'] != "Admin" and data["role"] != "User":
                    message ='role input can either be Admin or User'
                    return message

        #Validate common user data.
        for item in UserModel.user_fetch_data.keys():
            data_in_question = UserModel.user_fetch_data[item]
            if data_in_question['username'] == data['username']:
                message ='The username is already in the system'
                return message
            if data_in_question['email'] == data['email']:
                message ='The email already in use in the system.'
                return message

            if data_in_question['phone'] == data['phone']:
                message ='This phone number is in use'
                return message
        
        dict_user={
                    "username":data['username'],
                    "name":data['name'],
                    "email":data['email'],
                    "role":data["role"] if 'role' in data else "User",
                    "phone":data["phone"],
                    "password": generate_password_hash(str(data['password'])) 
                }

        #Add data to our store:
        UserModel.user_fetch_data[uuid.uuid4().hex] = dict_user
        return "CREATED"
    
    def login_user(self, data={}):
        '''This method allows the admin to create a user'''

        #Data validation
        if 'username' not in data or 'password' not in data:
            message ='Incomplete data!!'
            return message

        for item in UserModel.user_fetch_data.keys():
            data_in_question = UserModel.user_fetch_data[item]
            if data_in_question['username'] == data['username'] and check_password_hash(data_in_question['password'], data['password']):
                s = Serializer(Config.SECRET_KEY, expires_in=21600)
                token = (s.dumps({'user_id': item})).decode("ascii")
                return token

        return"Wrong Credentials!!"


    def no_of_users(self):
        return len(UserModel.user_fetch_data.keys())

    def list_of_users(self):
        return UserModel.user_fetch_data.keys()

    def get_person(self, user_id):
        if int(user_id) in UserModel.user_fetch_data.keys():
            return UserModel.user_fetch_data[int(user_id)]
        return False

    def delete_user(self, user_id):
        if int(user_id) in UserModel.user_fetch_data.keys():
            UserModel.user_fetch_data.pop(int(user_id))           
            return "DELETED"
        return False

        
    

