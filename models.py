import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

# referenced the implementation from fyyur project https://github.com/udacity/cd0046-SQL-and-Data-Modeling-for-the-Web/blob/master/app.py and also my local fyyur project

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/27a1ef74-4a77-4651-aca2-d701a408c3fd/concepts/cf6671dd-5249-4215-8207-dd9c677dc787?lesson_tab=lesson


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(255), nullable=True)
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
    restaurant = db.relationship('Restaurant', back_populates='menus')

    def __repr__(self):
        return f'<Menu(name={self.name}, price={self.price}, description={self.description}, available={self.available})>'
