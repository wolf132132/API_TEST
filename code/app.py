from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'zirong'
api = Api(app)

#JWT creates an end point, which is /auth
jwt = JWT(app, authenticate, identity)

items = []
  

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')

	"""
	next will return the first object it finds
	if it finds nothing, it will return None by putting None as a parameter
	"""
	@jwt_required()
	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item is not None else 404

	def post(self, name):
		if next(filter(lambda x: x['name'] == name, items), None) is not None:
			return {'message': 'Item has exsited already'}, 400
		data = Item.parser.parse_args()
		# create json payload
		# force=True means no content-header type required
		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201

	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
		else:
			item.update(data)
		return item


# name in <string:name> represents name in the get function as parameter
api.add_resource(Item, '/item/<string:name>')

app.run(port=5000, debug=True)
