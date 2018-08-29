from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel
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
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'item not found'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': 'Item {} has existed already'.format(name)}, 400
		data = Item.parser.parse_args()
		# create json payload
		# force=True means no content-header type required
		item = ItemModel(name, data['price'])
		try:
			ItemModel.insert(item)
		except:
			return {'message': 'An internal error occurs'}, 500
		return item.json(), 201

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
		item = ItemModel.find_by_name(name)
		updated_item = ItemModel(name, data['price'])

		if item is None:
			updated_item.insert()
		else:
			updated_item.update()
		return updated_item.json()


class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('database.db')
		cursor = connection.cursor()
		query = "SELECT * FROM items"
		result = cursor.execute(query)
		items = []
		for row in result:
			items.append({'name': row[0], 'price': row[1]})
		connection.close()

		return {'items': items}
