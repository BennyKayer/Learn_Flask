import sqlite3
from flask_restful import Resource, reqparse  # pylint: disable=import-error
from flask_jwt import jwt_required  # pylint: disable=import-error


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
        row = self.find_by_name(name)
        if row:
            return {"item": {"name": row[0], "price": row[1]}}, 200
        else:
            return {"message": "Item not found"}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()
        return row

    def post(self, name):
        # Check for duplicate <- error first approach
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": f"An item with name {name} already exists"}, 400

        request_data = Item.parser.parse_args()
        # Create new item and update db
        new_item = {"name": name, "price": request_data["price"]}

        connection = sqlite3.connect()
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, tuple(new_item.values()))

        connection.commit()
        connection.close()

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
