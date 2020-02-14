from flask import Flask, request
from flask_restful import Resource, Api  # pylint: disable=import-error

app = Flask(__name__)
api = Api(app)

items = []


class Items(Resource):
    def get(self):
        return {"items": items}, 200


api.add_resource(Items, "/items")


class Item(Resource):
    def get(self, name):
        """
        Gets an item with specified name
        
        Arguments:
            name {string} -- name of an item to
        
        Returns:
            dict -- item with price and name fields
        """

        item = dict(filter(lambda x: x["name"] == name, items))
        return item, 200 if bool(item) else 404

    def post(self, name):
        request_data = request.get_json()
        new_item = {"name": name, "price": request_data["price"]}
        items.append(new_item)
        return new_item, 201

    def delete(self, name):
        pass

    def put(self, name):
        pass


api.add_resource(Item, "/item/<string:name>")

# app.run(port=5000, debug=True) # if not using flask run
