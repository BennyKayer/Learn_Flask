import sqlite3
from flask_restful import Resource, reqparse  # pylint: disable=import-error


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # always tuple
        row = result.fetchone()
        if row:
            user = self(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(self, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))  # always tuple
        row = result.fetchone()
        if row:
            user = self(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", help="Provide username", required=True, type=str)
    parser.add_argument("password", help="Provide password", required=True, type=str)

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
