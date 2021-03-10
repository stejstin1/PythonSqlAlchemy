import sqlite3
from models.user import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="you need to input a password")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="you need to imput a password")


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201