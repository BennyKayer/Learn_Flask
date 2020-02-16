import sqlite3
from flask_restful import Resource, reqparse  # pylint: disable=import-error
from flask_jwt import jwt_required  # pylint: disable=import-error


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

    @classmethod
    def insert(cls, new_item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, tuple(new_item.values()))

        connection.commit()
        connection.close()

    def post(self, name):
        # Check for duplicate <- error first approach
        if self.find_by_name(name):
            return {"message": f"{name} already exists"}, 400

        request_data = Item.parser.parse_args()
        # Create new item and update db
        new_item = {"name": name, "price": request_data["price"]}

        try:
            self.insert(new_item)
        except:
            return {"message": "Error occured during inserting"}, 500

        return new_item, 201

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
        item = self.find_by_name(name)
        # Create / update accordingly
        updated_item = {"name": name, "price": request_data["price"]}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "Error during inserting"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "Error during updating"}, 500
        return updated_item, 200

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()
