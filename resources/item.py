from models.item import ItemModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank!") #Can use this req parser to also go through form fields from html..may need to look into that!

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #might need tto update with marchmellow?
        return {'message': 'Item not found'}, 404

    def post(self, name):
        #data = request.get_json()#force = true means you do not need a content-type header, silent = true makes it return none if it errors
        if ItemModel.find_by_name(name):
            return {'Message': "this '{}' already exists in the database".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except Exception as e:
            #print("error: ", e)
            return {'message': "an error occured inserting the item"}, 500

        return item.json(), 201 #Created status code, 202 is accepted

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'Message': "Item has been deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json() #anywhere with .json might be with marshmellow?



class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #loops through all the items from the query and jsonifies it