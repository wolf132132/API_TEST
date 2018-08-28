from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')

	"""
	next will return the first object it finds
	if it finds nothing, it will return None by putting None as a parameter
	"""
	@jwt_required()
	def get(self, name):
		item = self.find_by_name(name)
		if item:
			return item
		return {'message': 'item not found'}, 404

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('database.db')
		cursor = connection.cursor()
		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()
		if row:
			return {'items': {'name': row[0], 'price': row[1]}}

	def post(self, name):
		if self.find_by_name(name):
			return {'message': 'Item {} has existed already'.format(name)}, 400
		data = Item.parser.parse_args()
		# create json payload
		# force=True means no content-header type required
		item = {'name': name, 'price': data['price']}
		connection = sqlite3.connect('database.db')
		cursor = connection.cursor()
		query = "INSERT INTO items VALUES (?, ?) "
		cursor.execute(query, (item['name'], item['price']))
		connection.commit()
		connection.close()
		return item, 201

	def delete(self, name):
		connection = sqlite3.connect('database.db')
		cursor = connection.cursor()
		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))
		connection.commit()
		connection.close()

		return {'message': 'item has been deleted'}

	def put(self, name):
		data = Item.parser.parse_args()
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
		else:
			item.update(data)
		return item


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('database.db')
		cursor = connection.cursor()
		query = "SELECT * FROM items"
		cursor.execute(query)
