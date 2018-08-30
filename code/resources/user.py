import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'The username has existed'}, 400
        user = UserModel(data['username'], data['password']) #user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User has been created successfully'}, 201
