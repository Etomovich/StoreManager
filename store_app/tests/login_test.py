import unittest
import json
from flask import request
from store_app import create_app
from Instance.config import Config

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class LoginTests(unittest.TestCase):
    '''
       Purpose of this class is to set up all the dat that will be requit=red to run tests.
       This will include a registered user and a token for all methods that will required 
       a user to be logged in
    '''

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.root_access = json.dumps({
                        "username": "etomovich",
                        "password": "etomovich"
                        })

        self.user_1=({
                    "username":"pato",
                    "name":"Patrick Musau",
                    "email":"pato@musau.com",
                    "phone":"05677823158",
                    "password":'pato123',
                    "retype_password":"pato123"  
                })

        self.valid_credentials = json.dumps(
            {"username": "pato", "password": "pato123"})
        self.invalid_credentials = json.dumps(
            {"username": "pato", "password": "etyy"})

        self.context = self.app.app_context()
        self.context.push()

    
    def test_landing_endpoint(self):
        #Get Token
        admin_message = self.client.get("/api/v1/", content_type='application/json')
        
        self.assertEqual(admin_message.status_code,200,msg="Welcome endpoint not functioning as it should.")
    
    
    def test_login_user(self):
        admin_message = self.client.post("/api/v1/login",
                                            data=self.root_access,
                                            content_type='application/json')
        
        self.assertEqual(admin_message.status_code,200,msg="Root user has a login error.")
        

        def test_create_user(self):
            s = Serializer(Config.SECRET_KEY, expires_in=21600)
            token = s.dumps({'username': 'etomovich'})
            admin_message = self.client.post("/api/v1/admin/users",
                                            data=self.user_1,
                                            content_type='application/json')
        
        self.assertEqual(admin_message.status_code,201,msg="Admin should have ability to create users")

if __name__ == "__main__":
    unittest.main(verbosity=2)
