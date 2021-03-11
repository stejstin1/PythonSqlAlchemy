from db import db

class NewMixin:
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()