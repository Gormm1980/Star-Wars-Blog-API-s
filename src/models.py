from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BasicModel():
    @classmethod
    def get_all(cls):
        return cls.query.all()
        

    @classmethod
    def get_one(cls,id):
        return cls.query.get(id)
    
    @classmethod
    def delete(cls,id):
        return cls.query.delete(id)

class User(db.Model, BasicModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Character(db.Model, BasicModel):
    id_character = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (35))
    gender = db.Column(db.String (10))
    homeworld = db.Column(db.String (35))
    height = db.Column(db.Integer)
    species = db.Column(db.String (35))


    # def __repr__(self):
    #     return '<User %r>' % self.username

    def serialize(self):
        return {
            "id_character": self.id_character,
            "name": self.name,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "heigth": self.heigth,
            "species": self.species
            # do not serialize the password, its a security breach
        }
class Planets(db.Model, BasicModel):
    id_planet = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (35))
    climate = db.Column(db.String (10))
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String (35))

    # def __repr__(self):
    #     return '<User %r>' % self.username

    def serialize(self):
        return {
            "id_planet": self.id_planet,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "population": self.population,
            "terrain": self.terrain
            # do not serialize the password, its a security breach
        }
    
def session(self):        
        db.session.add(self)
        db.session.commit()
    
def set_with_character(self,json):
        self.name = json["name"]
        self.gender = json["gender"]
        self.homeworld = json["homeworld"]
        self.gender = json["gender"]
        self.height = json["height"]
        self.species = json["species"]

def set_with_planet(self,json):
        self.name = json["name"]
        self.climate = json["climate"]
        self.diameter = json["diameter"]
        self.population = json["population"]
        self.terrain = json["terrain"]
       

# class favorites(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     id_fav_planets = db.Column(db.Integer, ForeignKey('planets.id_planet'))
#     planets = db.relationship(Planets)
#     id_fav_characters = db.Column(db.Integer, ForeignKey('characters.id_character'))
#     character = db.relationship(Character)
#     favorites = db.Column(db.Integer, ForeignKey('user.id_user'))
#     user = db.relationship(User)

#     # def __repr__(self):
#     #     return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "id_fav_planets": self.id_fav_planets,
#             "planets ": self.planets,
#             "id_fav_characters": self.id_fav_characters,
#             "character": self.character,
#             "favorites": self.favorites,
#             "user":self.user
#             # do not serialize the password, its a security breach
#         }