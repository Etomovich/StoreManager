import uuid
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

from Instance.config import Config

class UserModel(object):
    '''This class allows a user to implement CRUD on a user object 
    '''
    user_fetch_data={'deee5d4e7eac420cb53179d1b9154a92':
                {
                    "username":"etomovich",
                    "name":"James Etole",
                    "email":"etolejames@gmail.com",
                    "role":"Admin",
                    "phone":"0717823158",
                    "password":""  
                }
            }
   

    def create_user(self, data={}):
        '''This method allows the admin to create a user'''

        #Data validation
        if 'Authorization' not in data or 'username' not in data or 'name' not in data or 'email' not in data  or 'phone' not\
                                                in data  or 'password' not in data or 'retype_password' not in data:
            message ='Incomplete data!!'
            return message
        for key in data.keys():
            if key == 'Authorization':
                s = Serializer(Config.SECRET_KEY)
                try:
                    authorized = s.loads(data['Authorization'])
                except:
                    message ='Wrong Authorization Key'
                    return message

                ##Check if user exists and is admin
                user_token = authorized['user_id']
                try:
                    user_data = UserModel.user_fetch_data[user_token]
                    if user_data['role'] != "Admin":
                        message ='This is an admin view'
                        return message
                except:
                    message ='Updater cannot be located'
                    return message

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
                if not(data['role'] is "Admin" or data['role'] is "User") :
                    message ='Role can either be Admin or User'
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

        

                

        

