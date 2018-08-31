from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
	parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id')

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
		item = ItemModel(name, data['price'], data['store_id'])
		try:
			ItemModel.save_to_db(item)
		except:
			return {'message': 'An internal error occurs'}, 500
		return item.json(), 201

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {'message': 'deleted from db'}

	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']

		item.save_to_db()

		return item.json()


class ItemList(Resource):
	def get(self):
		#return {'items': [item.json() for item in ItemModel.query.all()]}
		return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
