from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

# authentication
from security import authenticate, identity

# Resorces
from resources.user import UserRegister, User
from resources.item import Item, Items
from resources.store import Store, StoreList


app = Flask(__name__)
# can be postgres etc
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# without it flask app will just throw 500
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "dont_show_me_on_gh"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # creates /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

# Python will run everything outside methods / classes on import
if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)  # if not using flask run
