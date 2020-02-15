from flask import Flask
from flask_restful import Api  # pylint: disable=import-error
from flask_jwt import JWT  # pylint: disable=import-error

# authentication
from security import authenticate, identity

# Resorces
from resources.user import User
from resources.item import Item, Items


app = Flask(__name__)
app.secret_key = "dont_show_me_on_gh"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(User, "/register")
api.add_resource(Items, "/items")

# Python will run everything outside methods / classes on import
# if __name__ == "__main__":
# app.run(port=5000, debug=True) # if not using flask run
