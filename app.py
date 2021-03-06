import os

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from flask_migrate import Migrate
from dotenv import load_dotenv

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Items, Item
from db import db
from ma import ma

app = Flask(__name__)
load_dotenv(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI",'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This turns of the flask sqlalchemy tracker to save memory
app.secret_key = 'stephen'
api = Api(app)
migrate = Migrate(app,db)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #JWT creates a new endpoint called /auth

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

@app.route('/')
def Hello():
    return "This app is running"

#if __name__ == '__main__': #interesting error with flask migrate..if I have this here an assertion error happens
db.init_app(app)
ma.init_app(app)
app.run(host="0.0.0.0", port=9000, debug=True)