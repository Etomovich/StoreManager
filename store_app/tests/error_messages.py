import unittest
from store_app.api.version1.errors import error_response

class PaginationCase(unittest.TestCase):
    def test_error_response_feeback(self):
        message ='Bad request'
        answ= error_response(404,message)
        expected={"error":"Not Found","message":'Bad request'}

        self.assertEqual(answ,expected,msg="Kurasa paginator not working as expected")


if __name__ == "__main__":
    unittest.main(verbosity=2)