from db import db
from new_mixin import NewMixin

class ItemModel(db.Model, NewMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    @classmethod
    def find_by_name(cls, name:str):
        #Returns an ItemModel Object
        return cls.query.filter_by(name=name).first()# SELECT * FROM __tablename__ where name=name LIIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()