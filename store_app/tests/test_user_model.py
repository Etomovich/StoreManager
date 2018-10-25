import unittest
from Instance.config import Config
from store_app.api.version1.models import user_model
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.user_1= {
                "username":"etomovich",
                "name":"James Etole",
                "email":"etolejames@gmail.com",
                "role":"Admin",
                "phone":"0717823158",
                "password":"etole123",
                'retype_password':'etole123'
            }

        self.user_2= {
                "username":"pogie",
                "name":"Paul Pogba",
                "email":"paulpogba@gmail.com",
                "role":"User",
                "phone":"07157674544548",
                "password":"pogie",
                'retype_password':'pogie'
            }


    def test_create_user_from_root(self):
        users_DB = user_model.UserModel()
        answ = users_DB.create_user(self.user_1)
        self.assertEqual(answ,"CREATED", msg="There is an error when creating user with valid credentials")
        #remove user after test

    def test_create_user_with_bad_email(self):
        self.user_2["email"]='pogba_thee_og'
        users_DB = user_model.UserModel()
        answ = users_DB.create_user(self.user_2)

        self.assertEqual(answ,'Incorrect email format', msg="A user cannot be created with invalid data")

    def test_password_and_retype_pasword_not_equal(self):
        self.user_2["password"] ="paka"
        users_DB = user_model.UserModel()
        answ = users_DB.create_user(self.user_2)
        self.user_2['password'] = "pogie"

        self.assertEqual(answ,"Retype password and password should be equal.", msg="A user cannot be created with invalid data")

    def test_role_either_admin_or_user(self):
        self.user_2["role"] ="paka"
        users_DB = user_model.UserModel()
        answ = users_DB.create_user(self.user_2)
        self.user_2['role'] = "User"

        self.assertEqual(answ,"Role can either be Admin or User", msg="A user cannot be created with invalid data")
    
    def test_user_login_for_correct_user(self):
        users_DB = user_model.UserModel()
        answ = users_DB.login_user({"username":"etomovich", "password":"etomovich"})
        self.assertFalse(answ=='Incomplete data!!', msg="Login user not working correctly")

    def test_user_login_for_incomplete_credentials(self):
        users_DB = user_model.UserModel()
        answ = users_DB.login_user({"username":"etomovich"})
        self.assertTrue(answ=='Incomplete data!!', msg="Login user not working correctly")

    def test_user_login_for_wrong_credentials(self):
        users_DB = user_model.UserModel()
        answ = users_DB.login_user({"username":"etomovich", "password":"password"})
        self.assertFalse(answ=='Incomplete data!!', msg="Login user not working correctly")







    
