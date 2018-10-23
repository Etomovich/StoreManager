from flask import Blueprint

bp = Blueprint("api_version1", __name__)

users = {
     "etomovich":
                {
                    "name":"James Etole",
                    "email":"etolejames@gmail.com",
                    "role":"Admin",
                    "phone":"0717823158",
                    "password":'pbkdf2:sha256:50000$0cqd8PAJ$cf9e33813d77fae6939eca1219d87296ab59e793c0249b7b0267ab2bd0f8d3d8'  
                }
}
userslist=["etomovich"]## Stores the users

categories={
    "Drinks":[{"product_id": 45, "product_name":"Dasani 1/2 litre"},{"product_id": 34, "product_name":"Fanta 1 litre"}],
    "Sugar":[{"product_id": 212, "product_name":"Mumias Sugar 2 kg"},{"product_id": 423, "product_name":"Nzoia sugar 5kg"}]
}
list_of_categories = [{"category_name":"Drinks","Drinks":"This category is for all products that can be ingested by drinking"},{"category_name":"Sugar","Sugar":"All sugar items are to be placed in this category"}]

products ={
        1:{
            "product_details":{"product_name":"Kiwi 300g","product_description":"A shoe polish that....","amount_in_stock":9,"price":75,"category":"Rangi"},
            "items_in_stock":[1,2,3,4,5]
        },
        2:{
            "product_details":{"product_name":"Piclue","product_description":"A picule that....","amount_in_stock":9,"price":75,"category":"Pacta"},
            "items_in_stock":[]
        }
    }

items_in_stock={
     1:{"item_name":"Kiwi 300g","serial_no":"rttrfhy","expiration":"2018-08-13","product_id":1, "state":"ON_SHELF"},
     2:{"item_name":"Kiwi 300g","serial_no":"timto","expiration":"2018-08-13","product_id":1, "state":"ON_SHELF"},
     3:{"item_name":"Kiwi 300g","serial_no":"timto2","expiration":"2018-08-13","product_id":1, "state":"ON_SHELF"},
     4:{"item_name":"Kiwi 300g","serial_no":"timto3","expiration":"2018-08-13","product_id":1, "state":"ON_SHELF"},
     5:{"item_name":"Kiwi 300g","serial_no":"timto4","expiration":"2018-08-13","product_id":1, "state":"ON_SHELF"}
}

list_of_items=[{"item_id":1}, {"item_id":2}, {"item_id":3},{"item_id":4}, {"item_id":5} ]
recovered_item_ids=[]
list_of_products=[{1:"Kiwi 300g"},{2:"Dasani 1/2 litre"},{3:"Fanta 1 litre"}]
recovered_product_ids=[]

from store_app.api.version1.user_resources import the_api
from store_app.api.version1 import pagination,errors,user_resources,category,product_resources