import unittest
import json
import flask
from flask import request
from store_app import create_app
from Instance.config import Config
from store_app.api.version1.category import CreateCategoryAdmin

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class LoginTests(unittest.TestCase):
    '''
       This test suite checks on category.
    '''
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()

        
    def test_get_category_items(self):
        answ= self.client.get("/api/v1/category",
                                            content_type='application/json')
        output = json.loads(answ.data.decode())
        res= output

        self.assertEqual(res['Status'],"OK", msg="Get all categories not working")
        self.assertEqual(answ.status_code,200,msg="Get all categories not working")







        