import unittest
import json
from flask import Flask,request
from store_app import create_app

class LoginTests(unittest.TestCase):
    '''
       Purpose of this class is to set up all the dat that will be requit=red to run tests.
       This will include a registered user and a token for all methods that will required 
       a user to be logged in
    '''

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.default = json.dumps(
            {"username": "etomovich", "password": "etomovich"})

        self.valid_credentials = json.dumps(
            {"username": "pato", "password": "pato123"})
        self.invalid_credentials = json.dumps(
            {"username": "pato", "password": "etyy"})
        self.blank_credentials = json.dumps({"username": '', 'password': ''})

        self.user_1={
                    "username":"pato",
                    "name":"Patrick Musau",
                    "email":"pato@musau.com",
                    "phone":"05677823158",
                    "password":'pato123'  
                }
        self.user_2={
                    "username":"pogie",
                    "name":"Paul Pogba",
                    "email":"pogie123@gmail.com",
                    "phone":"045677",
                    "password":'pogie'  
                }
            

    def get_root_access(self):
        '''
           Check Root user
        '''
        response2 = self.client.post('/api/v1/login', data=self.default,content_type='application/json')                                             
        output = json.loads(response2.get_data())
        token = output.get('Authorization')
        return {'Authorization':  token}

    def test_registration_with_valid_credentials(self):
        '''Tests that a user is registered successfully'''

        access = self.get_root_access()
        response = self.client.post('/api/v1/admin/users', data=self.valid_credentials,headers={"Authorization":access['Authorization']},content_type='application/json')
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main(verbosity=2)