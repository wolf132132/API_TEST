from flask_restful import Resource
from models.store_model import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {store.json()}
        return {'message': 'store was not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'store exists already'}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'server error'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {'message': 'store does not exist'}
        store.delete_from_db()

        return {'message': 'store has been deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
