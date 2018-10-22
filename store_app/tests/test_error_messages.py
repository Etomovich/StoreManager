import unittest
import json
from store_app.api.version1.errors import error_response
from store_app import create_app

class ErrorResponcesCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.message ='ERROR'
        self.context.push()


    def test_error_response_feeback_400(self):
        answ= error_response(400,self.message)
        output = json.loads(answ.data.decode())
        expected={"error":"Bad Request","message":'ERROR'}

        self.assertEqual(output,expected,msg="error_responce not working properly")

if __name__ == "__main__":
    unittest.main(verbosity=2)