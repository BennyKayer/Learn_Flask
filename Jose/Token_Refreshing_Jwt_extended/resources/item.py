from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required,
)
from models.item import ItemModel


class Items(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {"items": items}, 200
        return (
            {
                "items": [item.json()["name"] for item in ItemModel.query.all()],
                "message": "More data available for logged users",
            },
            200,
        )


class Item(Resource):
    # Parse to avoid adding unwanted fields
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", help="Price must be provided", required=True, type=float
    )
    parser.add_argument(
        "store_id", help="Every item needs a store id", required=True, type=int
    )

    @jwt_required
    def get(self, name: str) -> dict:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 400

    @fresh_jwt_required
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

    @jwt_required
    def delete(self, name: str) -> dict:
        # jwt makes sure that only logged users will get there
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privileges required"}

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

