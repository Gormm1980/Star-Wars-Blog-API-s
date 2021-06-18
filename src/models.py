from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BasicModel():
    @classmethod
    def get_all(cls):
        return cls.query.all()
        

    @classmethod
    def get_one(cls,model_id):
        return cls.query.filter_by(id = model_id).first()
    
    @classmethod
    def delete(cls,self):
        return cls.query.delete()

class User(db.Model, BasicModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    token = db.Column(db.String(250), nullable=True)
    favorite_planets = db.relationship('Favorite_Planet', backref='user', lazy=True)


    @staticmethod
    def login_credentials(email,password):
        return User.query.filter_by(email=email).filter_by(password=password).first()
    
    
    def user_have_token(self,token):
        return User.query.filter_by(token=self.token).first()
   
    def assign_token(self,token):
        self.token = token
        db.session.add(self)
        db.session.commit()
    
    def check_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model, BasicModel):
    __tablename__ = 'people'
    id_people = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (35))
    gender = db.Column(db.String (10))
    homeworld = db.Column(db.String (35))
    height = db.Column(db.Integer)
    species = db.Column(db.String (35))

    def db_post(self):        
        db.session.add(self)
        db.session.commit()
    
    def set_with_people(self,json):
        self.name = json["name"]
        self.gender = json["gender"]
        self.homeworld = json["homeworld"]
        self.height = json["height"]
        self.species = json["species"]
        return self

    def serialize(self):
        return {
            "id_people": self.id_people,
            "name": self.name,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "height": self.height,
            "species": self.species
            # do not serialize the password, its a security breach
        }
class Planets(db.Model, BasicModel):
    __tablename__ = 'planets'
    id_planet = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (35))
    climate = db.Column(db.String (10))
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String (35))

    def serialize(self):
        return {
            "id_pleanets": self.id_planets,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "population": self.population,
            "terrain": self.terrain
            # do not serialize the password, its a security breach
        }
    
    def db_post(self):        
        db.session.add(self)
        db.session.commit()

    def set_with_planet(self,json):
        self.name = json["name"]
        self.climate = json["climate"]
        self.diameter = json["diameter"]
        self.population = json["population"]
        self.terrain = json["terrain"]
        return self
        
class Favorite_Planet(BasicModel,db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id_planet'))
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id":self.planet_id,
            }
