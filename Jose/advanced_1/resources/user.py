from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from blacklist import BLACKLIST
from typing import Tuple
from enum import Enum


NO_BLANK = "This field cannot be blank."
USER_EXISTS = "A user with that username already exists."
CREATED = "User created successfully."
NOT_FOUND = "User not found."
DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
LOGOUT = "User <id={}> successfully logged out."


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help=NO_BLANK)
_user_parser.add_argument("password", type=str, required=True, help=NO_BLANK)


class UserRegister(Resource):
    @classmethod
    def post(cls) -> Tuple:
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": USER_EXISTS}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int) -> Tuple:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int) -> Tuple:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls) -> Tuple:
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, data["password"]):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                200,
            )

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls) -> Tuple:
        jti = get_raw_jwt()[
            "jti"
        ]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return (
            {"message": LOGOUT.format(user_id)},
            200,
        )


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls) -> Tuple:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
