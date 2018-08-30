import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

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

