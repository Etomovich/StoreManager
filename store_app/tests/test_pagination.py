import unittest
from store_app.api.version1.pagination import Kurasa

class PaginationCase(unittest.TestCase):
    def test_kurasa_class_for_pagination(self):
        
        test_list = [1,3,4,5,6,7,8,9,5,6,67,2,3,5,6,7,8,7,5,3,2,3,5,6,7,8,8]
        test_list_1 = [3,4,5,6,7,9,5,6,67,2,3,5,6,7,8,7,5,3,2,3,5,6,7,8,8] 
        test_list_2 = []      
        kur = Kurasa(test_list, 5)
        kur2 = Kurasa(test_list_1, 5)
        kur3 = Kurasa(test_list_2, 5)

        #Testing even number of pages
        self.assertTrue(isinstance(kur2 , Kurasa),msg="Pagination should make a kurasa object")
        self.assertEqual(kur2.no_of_pages,6,msg="Kurasa paginator not working as expected")

        #Testing odd number of pages
        self.assertTrue(isinstance(kur , Kurasa),msg="Pagination should make a kurasa object")
        self.assertEqual(kur.no_of_pages,6,msg="Kurasa paginator not working as expected")

        #Check has next on an empty list
        self.assertEqual(kur3.has_next(2),False,msg="Kurasa paginator not working as expected")

        #check has next on last page
        self.assertEqual(kur.has_next(6),False,msg="Kurasa paginator not working as expected")

        #check has next if indeed next is there
        self.assertEqual(kur.has_next(3),True,msg="Kurasa paginator not working as expected")

        #check zero input
        self.assertEqual(kur.has_prev(0),False,msg="Kurasa paginator not working as expected")

        #check has next if indeed next is there
        self.assertEqual(kur.has_prev(2),True,msg="Kurasa paginator not working as expected")

        ##Get previous page
        self.assertEqual(kur.prev_page(3),2,msg="Kurasa paginator not working as expected")

        ##Get next page
        self.assertEqual(kur.next_page(3),4,msg="Kurasa paginator not working as expected")
    
        #check that it fetches correct items
        self.assertEqual(kur.get_items(3),[67, 2, 3, 5, 6],msg="Kurasa paginator not working as expected")




if __name__ == "__main__":
    unittest.main(verbosity=2)