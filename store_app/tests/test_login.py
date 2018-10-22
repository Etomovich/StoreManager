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

        self.incomplete_credentials = json.dumps(
            {"username": "etomovich", "password": ""})
            
        self.app = create_app("testing")
        self.client = self.app.test_client()
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

        output = json.loads(admin_message.data.decode())
        expected= "Login successful!! This token will be used to access all protected endpoints and will be valid for the next 6hrs then you will have to login again to access another token"
        
        self.assertEqual(output['message'],expected,msg="Admin should have ability to login to the system")
        
        self.assertEqual(admin_message.status_code,200,msg="Admin should have ability to login to the system")

    def test_login_wrong_user(self):
        admin_message = self.client.post("/api/v1/login",
                                            data=self.invalid_credentials,
                                            content_type='application/json')

        output = json.loads(admin_message.data.decode())
        expected={'message': 'user does not exist'}
        
        self.assertEqual(output,expected,msg="A user not in the system should not be allowed to log in")
        self.assertEqual(admin_message.status_code,401,msg="A  user not in the system should not be allowed to log in")

    def test_incomplete_credentials(self):
        answ= self.client.post("/api/v1/login",
                                            data=self.incomplete_credentials,
                                            content_type='application/json')
        output = json.loads(answ.data.decode())
        expected= {'message': 'You have entered a wrong password or username'}

        self.assertEqual(output,expected,msg="Incomplete credentials not allowed")


        


   

if __name__ == "__main__":
    unittest.main(verbosity=2)
