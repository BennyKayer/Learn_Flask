# Builtins
import traceback

# 3rd party
from flask import request, make_response, render_template
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from werkzeug.security import safe_str_cmp

# Local
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from models.user import UserModel
from schemas.user import UserSchema

# Consts
CREATED_SUCCESSFULLY = "Account created successfully, an emaill with an activation link has been sent to your email address"
FAILED_TO_CREATE = "Failed to create"
INVALID_CREDENTIALS = "Invalid credentials!"
NOT_ACTIVATED = "Account was not activated"
USER_ALREADY_EXISTS = "A user with that username already exists."
USER_CONFIRMED = "User successfully confirmed"
USER_DELETED = "User deleted."
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
USER_NOT_FOUND = "User not found."

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.email):
            return {"message": USER_ALREADY_EXISTS}, 400

        try:
            user.save_to_db()
            user.send_confirmation_email()
            return {"message": CREATED_SUCCESSFULLY}, 201
        except MailGunException as mge:
            user.delete_from_db()
            return {"message": str(mge)}, 500
        except:
            traceback.print_exc()
            return {"message": FAILED_TO_CREATE}, 500


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        user = UserModel.find_by_username(user_data.username)

        # Password first otherwise it's easier to hack
        if user and safe_str_cmp(user_data.password, user.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
            else:
                return {"message": NOT_ACTIVATED}

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"message": USER_NOT_FOUND}, 404

        user.activated = True
        user.save_to_db()
        headers = {"Content-Type": "text/html"}
        # return redirect("http://localhost:5000", 302)
        return make_response(
            render_template("confirmation_page.html", email=user.username), 200, headers
        )

