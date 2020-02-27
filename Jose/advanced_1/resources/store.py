from flask_restful import Resource
from models.store import StoreModel
from typing import Tuple
from enum import Enum


STORE_EXISTS = "A store with name '{}' already exists."
ERROR_CREATING = "An error occurred while creating the store."
NOT_FOUND = "Store not found."
DELETED = "Store deleted."


class Store(Resource):
    @classmethod
    def get(cls, name: str) -> Tuple:
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str) -> Tuple:
        if StoreModel.find_by_name(name):
            return (
                {"message": STORE_EXISTS.format(name)},
                400,
            )

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_CREATING}, 500

        return store.json(), 201

    @classmethod
    def delete(cls, name: str) -> Tuple:
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": DELETED}


class StoreList(Resource):
    @classmethod
    def get(cls) -> Tuple:
        return {"stores": [x.json() for x in StoreModel.find_all()]}
