import sqlite3
from flask_restful import Resource, reqparse  # pylint: disable=import-error
from flask_jwt import jwt_required  # pylint: disable=import-error
from models.item import ItemModel


class Items(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()
        return {"items": items}, 200


class Item(Resource):
    # Parse to avoid adding unwanted fields
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", help="Price must be provided", required=True, type=float
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "Item not found"}, 400

    def post(self, name):
        # Check for duplicate <- error first approach
        if ItemModel.find_by_name(name):
            return {"message": f"{name} already exists"}, 400

        request_data = Item.parser.parse_args()
        # Create new item and update db
        item = ItemModel(name, request_data["price"])

        try:
            item.insert()
        except:
            return {"message": "Error occured during inserting"}, 500

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()

        connection.close()

        return {"message": f"{name} deleted"}, 200

    def put(self, name):
        request_data = Item.parser.parse_args()
        # Check wheter item exists
        item = ItemModel.find_by_name(name)
        # Create / update accordingly
        updated_item = ItemModel(name, request_data["price"])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "Error during inserting"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "Error during updating"}, 500
        return updated_item.json(), 200

