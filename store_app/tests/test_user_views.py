import unittest
import json
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

        self.user_1={
                    "username":"pato",
                    "name":"Patrick Musau",
                    "email":"pato@musau.com",
                    "phone":"05677823158",
                    "password":'pato123',
                    "retype_password":"pato123"  
                }

        s = Serializer(Config.SECRET_KEY, expires_in=21600)
        self.root_access= (s.dumps({'user_id': 'deee5d4e7eac420cb53179d1b9154a92'})).decode("ascii")
        self.invalid_access= (s.dumps({'user_id': 'deee5d4e7e92'})).decode('ascii')

    
