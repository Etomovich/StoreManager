from flask import request, make_response, jsonify
from flask_restful import Resource, Api
from store_app.api.version1 import bp

the_api = Api(bp)

class Start(Resource):
    def get(self):
        return ({"message": "Welcome to Etomovich Stores."}, 200)

the_api.add_resource(Start, "/",'/welcome')