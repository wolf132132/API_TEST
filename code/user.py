import sqlite3
from flask_restful import Resource, reqparse


class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    """
    create the connection
    create the cursor
    set query
    execute query
    """
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))
        #this is going to return first row
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_query = "SELECT  * FROM users WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {'message': 'User has been created successfully'}, 201
