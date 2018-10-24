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

    def edit_user(self, data={}):
        if 'Authorization' not in data:
            message ='Please enter your authorization key!!'
            return message
        for key in data.keys():
            user_cre = ""
            bearer_role = False
            if key == 'Authorization':
                s = Serializer(Config.SECRET_KEY)
                try:
                    authorized = s.loads(data['Authorization'])
                except:
                    message ='Wrong Authorization Key'
                    return message

                ##Check if user exists and is admin
                user_cre = authorized['user_id']
                try:
                    user_data = UserModel.user_fetch_data[user_cre]
                    bearer_role= user_data['role'] 
                except:
                    message ='Updater cannot be located'
                    return message

            if bearer_role and bearer_role=="User":
                if "username" in data.keys() or "name" in data.keys() or "role" in data.keys():
                    message ='Note that you cannot change username,name and role as a User. Contact Admin for more help!!'
                    return message
                
                #check if is owner of details he/she wants to change
                if UserModel.user_fetch_data[user_cre]['username'] != data['user_changed']:#User_changed is url variable
                    message ='You cannot edit another persons credentials'
                    return message

                #Check validation and store valid changes the user makes
                changes = []
                for item in data.keys():
                    if key == 'email':
                        if data[key].find("@") < 2:
                            message ='Incorrect email format'
                            return message

                        changes.append("email")

                    if key == 'password':
                        if "retype_password" not in data.keys():
                            message ='You must enter a [retype_password] Key!!'
                            return message

                        if data['password'] != data["retype_password"]:
                            message ='Retype password and password should be equal.'
                            return message

                        changes.append("password")

                    if key == 'phone':
                        changes.append("phone")

                #Make the changes
                for item in changes:
                    UserModel.user_fetch_data[user_cre][item] = data[item]
                    message ='Edit completed succesfully.'
                    return message

            if bearer_role and bearer_role=="Admin":
                #Check validation and store valid changes the user makes
                changes = []
                for item in data.keys():
                    #Check email validation
                    if key == 'email':
                        if data[key].find("@") < 2:
                            message ='Incorrect email format'
                            return message

                        for item in UserModel.user_fetch_data.keys():
                            data_in_question = UserModel.user_fetch_data[item]
                            if data_in_question['email'] == data['email']:
                                message ='The email is already in the system'
                                return message

                        changes.append("email")

                    if key == 'password':
                        if "retype_password" not in data.keys():
                            message ='You must enter a [retype_password] Key!!'
                            return message

                        if data['password'] != data["retype_password"]:
                            message ='Retype password and password should be equal.'
                            return message

                        changes.append("password")

                    if key == 'phone':
                        for item in UserModel.user_fetch_data.keys():
                            data_in_question = UserModel.user_fetch_data[item]
                            if data_in_question['phone'] == data['phone']:
                                message ='The phone is already in the system'
                                return message

                        changes.append("phone")

                    if key == 'username':
                        for item in UserModel.user_fetch_data.keys():
                            data_in_question = UserModel.user_fetch_data[item]
                            if data_in_question['username'] == data['username']:
                                message ='The username is already in the system'
                                return 
                    
                    if key == 'role':
                        if not(data['role'] is "Admin" or data['role'] is "User") :
                            message ='Role can either be Admin or User'
                            return message
                        

            

                #Make the changes
                for item in changes:
                    UserModel.user_fetch_data[user_cre][item] = data[item]
                    message ='Edit completed succesfully.'
                    return message


        return "Updater not located"
        
    

