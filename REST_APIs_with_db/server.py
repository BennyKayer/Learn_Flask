from flask import Flask, request
from flask_restful import Resource, Api, reqparse  # pylint: disable=import-error
from flask_jwt import JWT, jwt_required  # pylint: disable=import-error
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = "dont_show_me_on_gh"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth

items = []


class Items(Resource):
    def get(self):
        return {"items": items}, 200


class Item(Resource):
    # Parse to avoid adding unwanted fields
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", help="Price must be provided", required=True, type=float
    )

    @jwt_required()
    def get(self, name):
        """
        Gets an item with specified name
        
        Arguments:
            name {string} -- name of an item to
        
        Returns:
            dict -- item with price and name fields
        """

        item = next(filter(lambda x: x["name"] == name, items), None)
        return item, 200 if item else 404

    def post(self, name):
        # Check for duplicate <- error first approach
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": f"An item with name {name} already exists"}, 400

        request_data = Item.parser.parse_args()
        # Create new item and update db
        new_item = {"name": name, "price": request_data["price"]}
        items.append(new_item)
        return new_item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": f"{name} deleted"}, 200

    def put(self, name):
        request_data = Item.parser.parse_args()
        # Check wheter item exists
        item = next(filter(lambda x: x["name"] == name, items), None)
        # Create / update accordingly
        if item is None:
            item = {"name": name, "price": request_data["price"]}
            items.append(item)
        else:
            item.update(request_data)
        return item, 200


api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")
api.add_resource(Items, "/items")

# app.run(port=5000, debug=True) # if not using flask run
