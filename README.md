[![Coverage Status](https://coveralls.io/repos/github/Etomovich/StoreManager/badge.svg?branch=ft-implement-create-user-161350147)](https://coveralls.io/github/Etomovich/StoreManager?branch=ft-implement-create-user-161350147)[![Build Status](https://travis-ci.org/Etomovich/StoreManager.svg?branch=ft-implement-create-user-161350147)](https://travis-ci.org/Etomovich/StoreManager.svg?branch=ft-implement-create-user-161350147)
**Etomovich Store Manager**

Etomovich Store Manager is an online Store management tool that enables store owners to oversee their business and store attendant to keep track of their sales per day.

In this develop branch I have Implemented the following routes:

|POST|**"/api/v1/register"**"->{"username":"user","name":"User User","email":"user@gmail.com","phone":"+00000","password":"user","retype_password":"user","role":"User"}
|**This route registers a new user using the data format displayed**.

|POST|**/api/v1/login**->{"username":"user","password":"user"}.|**This endpoint logs in a valid user who is in the system**

|GET|**api/v1/products**->[TAKES NO DATA]| **This route returns all products available inthe store**

|POST|**api/v1/products**->{"product_name":"Kimbo","price":"55"}|**This endpoint creates a new product. You can choose to add 'quatity'to show initial item count or forego. This is an admin only view.**

|GET|**api/v1/products/<productId> ->[TAKES NO DATA]| **This route returns a specific products available in the store by using the productsId**
  
|GET|**api/v1/products/search/<name>**->[TAKES NO DATA]| **This route returns search of the products that have <name> as a substring of thier product name**
  
|DELETE|**api/v1/products/delete/<productId>** -> [TAKES NO DATA]| **This route deletes a product. This is an admin view.**
  
|GET|**/api/v1/sales**|[TAKES NO DATA]|**Returns a list of all sales to have been recorded in the store. This is an Admin view**

|POST|**/api/v1/sales**{product id:quantity,product id:quantity}
  
  **Takes the product_ids of registered products and makes a sale. This view can only be viewed by attendant**
  
|GET|**/api/v1/sales/<saleId>** {product id:quantity,product id:quantity}
  
  **Takes the product_ids of registered products and quantity and makes a sale if applicable. This view can only be viewed by User(attendant)**

|GET|**api/v1/sales/search/<name>**|["TAKES NO DATA"]|**Provides the Admin with a view of the sales of an attendant. This is an Admin view**
  
 |DELETE|**api/v1/sales/delete/<saleId>** -> [TAKES NO DATA]| **This route deletes a sale. This is an Admin view.**
