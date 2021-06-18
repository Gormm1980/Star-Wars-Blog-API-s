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
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "153218879fwfs1saf1a8eafffs_ffasa+fap`+çsçç+7dçfafewr"  
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

@app.route("/users",methods=['GET'])
def all_users():
    people = User.get_all()
    people_dic = []
    for person in people :
        people_dic.append(person.serialize())
    return jsonify(people_dic),200
  
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

@app.route("/login", methods=['POST'])
def handle_login():

    json=request.get_json()

    if json is None: 
        raise APIException("You shoulld be return a json")

    if "email" not in json:
        raise APIException("That's not an email in json")

    if "password" not in json:
        raise APIException("That's not a password in json")
    
    print(json["email"],json["password"])
   
    email = json["email"]
    password = json["password"]

    user = User.query.filter_by(email=email).one_or_none()

    if user is None:
         raise APIException("User not found")

    if not user.check_password(password):
      return jsonify("Your credentials are wrong, please try again"), 401

    access_token = create_access_token(identity=user.serialize())
    return jsonify(accessToken=access_token)

@app.route("/profile", methods=['POST'])
def handle_profile():
    json = request.get_json()
    user = User.user_have_token(json["token"])
    if user is None :
        raise APIExeption("You don't have a token")

    return jsonify(user.serialize()),200


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    for user in users:
       if User.id == user:
        return user


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
