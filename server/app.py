#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

    api = Api(app)

class Plants(Resource):
    pass
    def get(self):
        plants_dict = [p.to_dict() for p in Plant.query.all()]

        response = make_response(jsonify(plants_dict), 200)

        return response

    def post(self):
        name = request.form.get('name')
        image = request.form.get('image')
        price = request.form.get('price')

        new_plant = Plant(name=name, image=image, price=price)

        db.session.add(new_plant)
        db.session.commit()

        response = make_response(jsonify(new_plant), 201)

        return response

api.add_resource(Plants, '/plants')    

class PlantByID(Resource):
    pass
    def get(self, id):
        plant_dict = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(jsonify(plant_dict), 200)

        return response

api.add_resource(PlantByID, '/plants/<int:id>')    


if __name__ == '__main__':
