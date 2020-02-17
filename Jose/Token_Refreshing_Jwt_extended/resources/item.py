from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Items(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


class Item(Resource):
    # Parse to avoid adding unwanted fields
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", help="Price must be provided", required=True, type=float
    )
    parser.add_argument(
        "store_id", help="Every item needs a store id", required=True, type=int
    )

    @jwt_required()
    def get(self, name: str) -> dict:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 400

    def post(self, name: str) -> dict:
        # Check for duplicate <- error first approach
        if ItemModel.find_by_name(name):
            return {"message": f"{name} already exists"}, 400

        request_data = Item.parser.parse_args()
        # Create new item and update db
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {"message": "Error occured during inserting"}, 500

        return item.json(), 201

    def delete(self, name: str) -> dict:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    def put(self, name: str) -> dict:
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data["price"]

        item.save_to_db()
        return item.json(), 200

