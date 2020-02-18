from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db


# Resorces
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, StoreList

# Blacklist
from blacklist import BLACKLIST

app = Flask(__name__)
# can be postgres etc
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# without it flask app will just throw 500
app.config["PROPAGATE_EXCEPTIONS"] = True
# Blacklisting tokens
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
# supposed to work - didn't
# app.secret_key = app.config["JWT_SECRET_KEY"]
app.secret_key = "ehh"
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # instead of hard-coding read from db
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


# What to do when token expires?
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"desc": "Token expired", "error": "token expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"desc": "Signature verification failed", "error": "invalid token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "desc": "Request does not contain access token",
                "error": "authorization required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify({"desc": "Token is not fresh", "error": "fresh_token_required"}),
        401,
    )


# Log out
@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify({"desc": "The token has been revoked", "error": "token_revoked"}),
        401,
    )


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserLogout, "/logout")

# Python will run everything outside methods / classes on import
if __name__ == "__main__":
    app.run(port=5000, debug=True)  # if not using flask run
