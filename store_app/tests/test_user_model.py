import unittest
from Instance.config import Config
from store_app.api.version1.models import user_model
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.user_1= {
                "username":"anthony",
                "name":"Anthony Kamau",
                "email":"kamau@gmail.com",
                "role":"User",
                "phone":"07157678",
                "password":"kama",
                'retype_password':'kama'
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

        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        self.root_access= (s.dumps({'user_id': 'deee5d4e7eac420cb53179d1b9154a92'})).decode("ascii")
        self.invalid_access= (s.dumps({'user_id': 'deee5d4e7e92'})).decode('ascii')


    def test_create_user_from_root(self):
        users_DB = user_model.UserModel()
        self.user_1['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_1)
        self.user_1.pop("Authorization")
        self.assertEqual(answ,"CREATED", msg="There is an error when creating user with valid credentials")
        #remove user after test

    def test_create_user_with_decodable_token_bt_user_is_not_in_system(self):
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.invalid_access
        answ = users_DB.create_user(self.user_2)
        self.user_2.pop("Authorization")
        self.assertEqual(answ,"Updater cannot be located", msg="Error when creating user")
        #remove user after test


    def test_create_user_with_incomplete_data(self):
        self.user_2.pop("username")
        users_DB = user_model.UserModel()
        self.user_1['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)
        self.user_2['username'] = "pogie"

        self.assertEqual(answ,"Incomplete data!!", msg="A user cannot be created with invalid data")

    def test_user_already_exists(self):
        self.user_2["username"] ="etomovich"
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)
        self.user_2['username'] = "pogie"

        self.assertEqual(answ,"The username is already in the system", msg="A user cannot be created with invalid data")

    def test_email_already_exists(self):
        self.user_2["email"] ="etolejames@gmail.com"
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)
        self.user_2['email'] = "paulpogba@gmail.com"

        self.assertEqual(answ,"The email already in use in the system.", msg="A user cannot be created with invalid data")

    def test_phone_already_exists(self):
        self.user_2["phone"] ="0717823158"
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)
        self.user_2['phone'] = "0717823158"

        self.assertEqual(answ,"This phone number is in use", msg="A user cannot be created with invalid data")

    def test_create_user_with_bad_email(self):
        self.user_2["email"]='pogba_thee_og'
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)

        self.assertEqual(answ,'Incorrect email format', msg="A user cannot be created with invalid data")

    def test_password_and_retype_pasword_not_equal(self):
        self.user_2["password"] ="paka"
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)
        self.user_2['password'] = "pogie"

        self.assertEqual(answ,"Retype password and password should be equal.", msg="A user cannot be created with invalid data")

    def test_role_either_admin_or_user(self):
        self.user_2["role"] ="paka"
        users_DB = user_model.UserModel()
        self.user_2['Authorization'] = self.root_access
        answ = users_DB.create_user(self.user_2)
        self.user_2['role'] = "User"

        self.assertEqual(answ,"Role can either be Admin or User", msg="A user cannot be created with invalid data")


