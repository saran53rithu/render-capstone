import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#database_url = "postgresql://postgres:password@localhost:5432/postgres"

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_url=database_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    
    # Relationship with Menu table; no backref to avoid conflicts
    menus = db.relationship('Menu', back_populates='restaurant', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Restaurant(name={self.name}, address={self.address}, phone_number={self.phone_number}, email={self.email})>'

class Menu(db.Model):
    __tablename__ = 'menu'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
    # Relationship with Restaurant table; no backref to avoid conflicts
    restaurant = db.relationship('Restaurant', back_populates='menus')

    def __repr__(self):
        return f'<Menu(name={self.name}, price={self.price}, description={self.description}, available={self.available})>'