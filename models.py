from flask import Flask
from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, SmallInteger, String, Text, text, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



# constructor method
db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(String(150), nullable=False, unique=True)

    recipes = db.relationship('Recipe', backref='category', lazy='dynamic')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(String(150), nullable=False, unique=True)

    recipes = db.relationship('Recipe', backref='course', lazy='dynamic')

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(String(150), nullable=False, unique=True)

    recipes = db.relationship('Recipe', backref='cuisine', lazy='dynamic')

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(String(150), nullable=False, unique=True)
    author_country = db.Column(String(150))

    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer)
    step_description = db.Column(Text)

class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allergen_name = db.Column(String(150), nullable=False, unique=True)

db.Table('recipe_allergen',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('allergen_id', db.Integer, db.ForeignKey('allergen.id'))
    )

class Dietary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dietary_name = db.Column(String(150), nullable=False, unique=True)

db.Table('recipe_dietary',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('dietary_id', db.Integer, db.ForeignKey('dietary.id'))
    )

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(String(150), nullable=False, unique=True)
    recipe_description = db.Column(Text)
    preparation_time = db.Column(db.Integer)
    cooking_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    steps = db.relationship('Step', backref='recipe', lazy='dynamic')
    quantities = db.relationship('Quantity', backref='recipe', lazy='dynamic')
    allergens = db.relationship('Allergen', secondary='recipe_allergen', backref='recipe', lazy='dynamic')
    dietaries = db.relationship('Dietary', secondary='recipe_dietary', backref='recipe', lazy='dynamic')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(String(150), nullable=False, unique=True)

    quantities = db.relationship('Quantity', backref='ingredient', lazy='dynamic')

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_name = db.Column(String(150), nullable=False, unique=True)

    quantities = db.relationship('Quantity', backref='measurement', lazy='dynamic')


class Quantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurement.id'), nullable=False)
    quantity = db.Column(db.Float)
    