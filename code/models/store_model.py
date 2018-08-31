import sqlite3
from db import db

"""
@when user calls find_by_name, the method will return an item object. So the json() method will be required to return a dictionary
"""


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    '''
    @lazy=dynamic means that the property is not a list of objects, but a query(self.item) that we can run.
    @The benefit is that when we load the initial object, it does not have to load the related objects.
    @The drawback is that when we want to access the related objects, we have to query for them (using .all() in this case, as that runs the PostgreSQL query).
    @Whenever we created a store model, we are going to create an item model in the database
        match the store ID
    '''
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        #db.session is object itself
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

