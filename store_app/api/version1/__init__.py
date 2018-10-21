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

from store_app.api.version1.user_resources import the_api
from store_app.api.version1 import pagination,errors