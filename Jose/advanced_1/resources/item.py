from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel
from typing import Tuple


NO_BLANK = "{} cannot be left blank!"
ITEM_NOT_FOUND = "Item not found."
ITEM_EXISTS = "An item with name '{}' already exists."
ITEM_DELETED = "Item Deleted"
INSERTION_ERROR = "An error occurred while inserting the item."


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=NO_BLANK.format("price"),
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=NO_BLANK.format("store_id"),
    )

    @classmethod
    def get(cls, name: str) -> Tuple:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str) -> Tuple:
        if ItemModel.find_by_name(name):
            return (
                {"message": str(ITEM_EXISTS).format(name)},
                400,
            )

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": INSERTION_ERROR}, 500

        return item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str) -> Tuple:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str) -> Tuple:
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    @classmethod
    def get(cls) -> Tuple:
        return {"items": [item.json() for item in ItemModel.find_all()]}, 200
