from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return jsonify(item)
        return "Item does not exist", 400

    def post(self, name):
        request_data = request.get_json()
        new_item = {"name": name, "price": request_data["price"]}
        items.append(new_item)
        return new_item

    def delete(self, name):
        pass

    def put(self, name):
        pass


api.add_resource(Item, "/item/<string:name>")

