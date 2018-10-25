import uuid
from store_app.api.version1.models.products_model import Products

class Sales(object):
    fetch_sales={}
    recovered_fetch_ids=[]



    def create_sale(self, data={}):
        '''This method implements create product'''
        new_sale_id = uuid.uuid4().int

        if 'username' not in data:
            return "Please Enter [username]  to make this sale"

        username = data.pop('username')



        #check if all products are there
        for item in data.keys():
            try:
                prod_details = Products.fetch_products[item]               
            except:
                return "Product "+str(item)+" does not exist."

            try:
                quantity = int(data[item])              
            except:
                return "Product "+str(item)+" has an invalid amount."
        
        #Make the sale if all products are there
        total_amount = 0
        sold_items=[]
        for item in data.keys():
            prod_data = Products.fetch_products[item]
            total_amount = total_amount + (prod_data['price'] * data[item])
            item_sale = {
                "Total": prod_data['price'] * data[item],
                "Price": prod_data['price'],
                "Pieces Sold": data[item],
                "product_name": prod_data['product_name']
            }
            #Decrement Product
            Products.fetch_products[item]['quantity'] -= data[item]
            sold_items.append(item_sale)

        reply = {
            "Total_Shopping_Totals": total_amount,
            "shopping_items": sold_items,
            "attendant": username
        }
        Sales.fetch_sales[new_sale_id] = reply
        return reply

    def search_for_sale(self, attendant):
        search_results=[]
        for item in Sales.fetch_sales.keys():
            if Sales.fetch_sales[item]['attendant'] == attendant:
                reply =Sales.fetch_sales[item]
                reply['sale_id'] = item
                search_results.append(reply)

        return search_results


    def no_of_sales(self):
        return len(Sales.fetch_sales.keys())

    def list_of_sales(self):
        return Sales.fetch_sales.keys()

    def get_sale_item(self, sales_id):
        if int(sales_id) in Sales.fetch_sales.keys():
            return Sales.fetch_sales[int(sales_id)]
        return False

    def delete_sale_item(self, sale_id):
        if int(sale_id) in Sales.fetch_sales.keys():
            Sales.fetch_sales.keys(int(sale_id))           
            return "DELETED"
        return False




        