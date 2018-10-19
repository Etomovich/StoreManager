import unittest
from store_app.api.version1.pagination import Kurasa

class PaginationCase(unittest.TestCase):
    def test_kurasa_class_for_pagination(self):
        
        test_list = [1,3,4,5,6,7,8,9,5,6,67,2,3,5,6,7,8,7,5,3,2,3,5,6,7,8,8]       
        kur = Kurasa(test_list, 5)
        self.assertEqual(kur.no_of_pages,6,msg="Kurasa paginator not working as expected")

        #kur.has_next takes in a page and returns True if there is a page after that one else false
        self.assertEqual(kur.has_next(3),True,msg="Kurasa paginator not working as expected")

        #kur.has_next takes in a page and returns True if there is a page before that one else false
        self.assertEqual(kur.has_prev(3),True,msg="Kurasa paginator not working as expected")
    
        #check that it fetches correct items
        self.assertEqual(kur.get_items(3),[67, 2, 3, 5, 6],msg="Kurasa paginator not working as expected")




if __name__ == "__main__":
    unittest.main(verbosity=2)