from store_app import create_app
from flask import json
import unittest



class WelcomeScreen(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()



    def test_welcome_to_store(self):
        '''
        Tests retrieving welcome message
        '''
        get_bucketlists = self.client.get('/api/v1/welcome', content_type='application/json' )
        self.assertEquals(get_bucketlists.status_code, 200)