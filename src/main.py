"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

  
@app.route("/people",methods=['GET'])
def all_people():
    people = People.get_all()
    people_Dic = []
    for person in people :
        people_Dic.append(person.serialize())
    return jsonify(people_Dic)

@app.route("/people",methods=['POST'])
def adding_people():
    json = request.get_json()
    print (json)
    people = People.set_with_people(People(),json)
    People.db_post(people)
    return jsonify(people.serialize())

@app.route("/people/<int:people_id>", methods=['GET'])
def one_people(people_id):
    people = People.get_one(people_id)
    people_serialized = people.serialized()
    return jsonify(people_serialized)

@app.route("/people/<int:people_id>", methods=["DELETE"])
def people_delete(people_id):
    people = People.query.get(people_id)
    People.delete(people)
    return jsonify(people.serialize())

@app.route("/planets", methods=["GET"])
def all_planets():
    planets = Planets.get_all()
    planets_Dic = []
    for planet in planets :
        planets_Dic.append(planet.serialize())
    return jsonify(planets_Dic)

@app.route("/planets",methods=['POST'])
def adding_planet():
    json = request.get_json()
    print (json)
    planets = planets.set_with_planet(json)
    planets.db_post(planets)
    return jsonify(planets.serialize())

@app.route("/planets/<planets_id>", methods=['GET'])
def one_planet(planets_id):
    planets = Planets.get_one(planets_id)
    planets_serialized = planets.serialized()
    return jsonify(planets_serialized)

@app.route("/planets/<planets_id>", methods=["DELETE"])
def planets_delete(planets_id):
    planets = Planets.query.get(planets_id)
    Planets.delete(planets)
    return jsonify(planets.serialize())

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    
    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
