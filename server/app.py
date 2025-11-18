#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
# Importing the update and delete functions from the controller
from controller.controller_plant import update_plant, patch_plant, delete_plant


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return {"error": "Plant not found"}, 404
        return make_response(jsonify(plant.to_dict()), 200)


class UpdatePlant(Resource):

    def put(self, plant_id):
        data = request.get_json()
        return update_plant(plant_id, data['name'], data['image'], data['price'], data['is_in_stock'])

    def patch(self, plant_id):
        data = request.get_json()
        return patch_plant(plant_id, data)


class DeletePlant(Resource):

    def delete(self, plant_id):
        return delete_plant(plant_id)


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
api.add_resource(UpdatePlant, '/plants/<int:plant_id>')
api.add_resource(DeletePlant, '/plants/<int:plant_id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
