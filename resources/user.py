from models.user import UserModel
from flask_restful import Resource
from flask import request
from schemas.user import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()

class UserRegister(Resource):
    def post(self):
        try:
            user = user_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_username(user.username):
            return {"message": "A user with that username already exists"}, 400

        #user = UserModel(**user_data) #was using before, but now the we are using sqlalch marshmallow we don't need
        # because we define our model with the correct fields we need! very interesting find!
        user.save_to_db()
        return {"message": "User created"}, 201