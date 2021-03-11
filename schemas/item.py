from ma import ma
from models.item import ItemModel

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ("id")
        dump_only = ("id",)
        load_instance = True