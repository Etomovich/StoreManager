import unittest
from store_app.api.version1.errors import error_response

class PaginationCase(unittest.TestCase):
    def test_error_response_feeback(self):
        message ='Bad request'
        answ= error_response(400,message)
        expected={"error":"Bad Request","message":'ERROR'}

        self.assertEqual(answ,expected,msg="error_responce not working properly")

        answ= error_response(404,message)
        expected={"error":"Not Found","message":'ERROR'}

        self.assertEqual(answ,expected,msg="error_responce not working properly")

        answ= error_response(401,message)
        expected={"error":"Unauthorized","message":'ERROR'}

        self.assertEqual(answ,expected,msg="error_responce not working properly")

        answ= error_response(403,message)
        expected={"error":"Forbidden","message":'ERROR'}

        self.assertEqual(answ,expected,msg="error_responce not working properly")

        answ= error_response(405,message)
        expected={"error":"Method Not Allowed","message":'ERROR'}

        self.assertEqual(answ,expected,msg="error_responce not working properly")

    def test_unknown_error(self):
        message ='ERROR'
        answ= error_response(2,message)
        expected={"error":"Unknown error","message":'ERROR'}

        self.assertEqual(answ,expected,msg="error_responce not working properly")
if __name__ == "__main__":
    unittest.main(verbosity=2)