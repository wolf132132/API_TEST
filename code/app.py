from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
#this is going to tell sql to find the databse bfile in the root dic
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.secret_key = 'zirong'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

#JWT creates an end point, which is /auth
jwt = JWT(app, authenticate, identity)

# name in <string:name> represents name in the get function as parameter
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
