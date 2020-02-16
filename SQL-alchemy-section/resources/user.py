from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", help="Provide username", required=True, type=str)
    parser.add_argument("password", help="Provide password", required=True, type=str)

    def post(self):
        data = User.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201
