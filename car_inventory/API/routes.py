from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


#Create Car endpoint

@api.route('/cars', methods = ['POST'])
@token_required
def create_drone(our_user):
    make = request.json['make']
    model = request.json['model']
    price = request.json['price']
    mpg = request.json['mpg']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    user_token = our_user.token
    

    print(f"User Token: {our_user.token}")

    car = Car(make, model, price, mpg, max_speed, dimensions, weight, cost_of_production, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


#retreive all car endpoints
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    owner = our_user.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)

    return jsonify(response)


#retreive one car endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401

#update car endpoint
@api.route('/cars/<id>', methods = ['PUT', 'POST'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.price = request.json['price']
    car.mpg = request.json['mpg']
    car.max_speed = request.json['max_speed']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.cost_of_production = request.json['cost_of_production']
    car.user_token = our_user.token
    response = car_schema.dump(car)
    return jsonify(response)


#delete car endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_cars(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)