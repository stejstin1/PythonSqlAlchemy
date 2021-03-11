from models.item import ItemModel
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from schemas.item import ItemSchema
from flask_jwt import jwt_required

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)
        return {'message': 'Item not found'}, 404

    def post(self, name:str): # /item/chair
        if ItemModel.find_by_name(name):
            return {'Message': "this '{}' already exists in the database".format(name)}, 400

        #data = Item.parser.parse_args()
        item_json = request.json # price
        item_json['name'] = name

        #item = ItemModel(name, data['price'])

        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.save_to_db()
        except:
            return {'message': "Error inserting item"}, 500

        return item_schema.dump(item), 201 #Created status code, 202 is accepted

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'Message': "Item has been deleted"}

    def put(self, name:str):
        item_json= request.json
        item = ItemModel.find_by_name(name)

        if item is None:
            item_json['name'] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400
        else:
            item.price = item_json['price']

        item.save_to_db()
        return item_schema.dump(item)



class Items(Resource):
    def get(self):
        return {'items': [item_list_schema.dump(ItemModel.find_all())]}