import unittest
import json
from flask import jsonify
from Instance.config import Config, TestingConfig
from store_app.api.version1.models import user_model
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from store_app import create_app

class UserViewsCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.user_1=json.dumps({"username":"anthony","name":"Anthony Kimani","email":"anto@gmail.com","phone":"+2546766734523","password":"kimani","retype_password":"kimani"})
        

    def test_create_user(self):
        answ= self.client.post("/api/v1/register",
                                            data=self.user_1,
                                            content_type='application/json')

        output = json.loads(answ.data.decode())
        self.assertEqual(output['Status'],"CREATED",msg="Incomplete credentials not allowed")
        self.assertEqual(answ.status_code,201,msg="Incomplete credentials not allowed")

    def test_login_user_correct(self):
        answ1= self.client.post("/api/v1/register",
                                            data=self.user_1,
                                            content_type='application/json')
        answ= self.client.post("/api/v1/login",
                                            data=json.dumps({"username":"anthony","password":"kimani"}),
                                            content_type='application/json')

        output = json.loads(answ.data.decode())
        self.assertEqual(output['Status'],"LoggedIn",msg="Incomplete credentials not allowed")
        self.assertEqual(answ.status_code,200,msg="Incomplete credentials not allowed")

    def test_login_user_wrong_data(self):
        answ1= self.client.post("/api/v1/register",
                                            data=self.user_1,
                                            content_type='application/json')
        answ= self.client.post("/api/v1/login",
                                            data=json.dumps({"username":"anthony","password":""}),
                                            content_type='application/json')

        output = json.loads(answ.data.decode())
        self.assertEqual(output['Status'],"Wrong Credentials!!",msg="Incomplete credentials not allowed")
        self.assertEqual(answ.status_code,401,msg="Incomplete credentials not allowed")

    
 


    
