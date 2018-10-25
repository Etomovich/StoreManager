import unittest
from store_app.api.version1.models import products_model

class ProductModelCase(unittest.TestCase):
    def setUp(self):
        self.product_1= {
                "product_name":"kiwwi 300g",
                "price": "45"
            }

        self.product_2= {
                "product_name":"Mango",
                "price": "45",
                "quantity": "70"
            }


    def test_create_product(self):
        prod = products_model.Products()
        answ = prod.create_product(self.product_1)

        self.assertEqual(answ,"CREATED", msg="create product not working as it should")


    def test_duplicate_product(self):
        prod = products_model.Products()
        a = prod.create_product(self.product_1)
        answ = prod.create_product(self.product_1)

        self.assertEqual(answ,"Product is already in the systemm!!", msg="create product not working as it should")

    def test_create_product_with_bad_price(self):
        prod = products_model.Products()
        answ = prod.create_product({"product_name":"Chilli","price":"paka"})

        self.assertEqual(answ,"Price must be a decimal or integer type!!", msg="create product not working as it should")

    def test_create_product_incomplete(self):
        prod = products_model.Products()
        answ = prod.create_product({"price":"34"})

        self.assertEqual(answ,"Incomplete data!!", msg="create product not working as it should")

    def test_search_product(self):
        prod = products_model.Products()
        a = prod.create_product(self.product_2)
        answ = prod.search_for_product("Mango")

        self.assertEqual(len(answ),1, msg="search product not working as it should")


    def test_get_product_item(self):
        prod = products_model.Products()
        answ = prod.list_of_products()

        self.assertTrue(isinstance(answ, list), msg="search product not working as it should")


    def test_get_no_of_products(self):
        prod = products_model.Products()
        answ = prod.no_of_products()

        self.assertEqual(len(answ),len(products_model.Products.fetch_products.keys()), msg="get no of products not working as it should")

    


