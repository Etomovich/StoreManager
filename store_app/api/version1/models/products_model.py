import uuid


class Products(object):
    fetch_products={}




    def create_product(self, data={}):
        '''This method implements create product'''
        new_product_id = uuid.uuid4().int

        if 'product_name' not in data or 'price' not in data:
            return "Incomplete data!!"

        for item in Products.fetch_products.keys():
            if Products.fetch_products[item]['product_name'] == data['product_name']:
                return "Product is already in the systemm!!"
        
        try:
            float(data['price'])
        except:
            return "Price must be a decimal or integer type!!"

        quantity = False
        #check if there is a quantity input
        try:
            quantity = data['quantity']
        except:
            quantity = False

        #check if quantity can be converted to INT type
        try:
            if quantity:
                quantity = int(quantity)
        except:
             return "Quantity should be an int!!"

        product_desc = False
         #check if there is a product_desc input
        try:
            product_desc = data['product_description']
        except:
            product_desc = False
        
        data_info ={
            "product_name": data['product_name'],
            "price": int(data['price']),
            "quantity": quantity if quantity else 0,
            "product_description": product_desc if product_desc else ""
        }
        Products.fetch_products[new_product_id]=data_info
        return "CREATED"

    def search_for_product(self, name):
        search_results=[]
        for item in Products.fetch_products.keys():
            if Products.fetch_products[item]['product_name'].find(name) >=0:
                reply =Products.fetch_products[item]
                reply['product_id'] = item
                search_results.append(reply)

        return search_results

    def no_of_products(self):
        return len(Products.fetch_products.keys())

    def list_of_products(self):
        gg=[]
        for item in Products.fetch_products.keys():
            ty ={}
            ty[item] = Products.fetch_products[item]
            gg.append(ty)
        
        return gg

    def get_product_item(self, product_id):
        if int(product_id) in Products.fetch_products.keys():
            return Products.fetch_products[int(product_id)]
        return False

    def delete_item(self, product_id):
        if int(product_id) in Products.fetch_products.keys():
            Products.fetch_products.pop(int(product_id))           
            return "DELETED"
        return False