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

    #recipes = db.relationship('Recipe', backref='category', lazy='dynamic')

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return '<Category %r>' % self.category_name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(String(150), nullable=False, unique=True)

    #recipes = db.relationship('Recipe', backref='course', lazy='dynamic')

    def __init__(self, course_name):
        self.course_name = course_name

    def __repr__(self):
        return '<Course %r>' % self.course_name

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(String(150), nullable=False, unique=True)

    #recipes = db.relationship('Recipe', backref='cuisine', lazy='dynamic')

    def __init__(self, cuisine_name):
        self.cuisine_name = cuisine_name

    def __repr__(self):
        return '<Cuisine %r>' % self.cuisine_name

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(String(150), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('authors', lazy=True))

    #recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    def __init__(self, author_name):
        self.author_name = author_name
    
    def __repr__(self):
        return '<Author %r>' % self.author_name

class Country(db.Model):
    id = Column(db.Integer, primary_key=True)
    country_name = db.Column(String(150), nullable=False, unique=True)
    
    def __init__(self, country_name):
        self.country_name = country_name
    
    def __repr__(self):
        return '<Country %r>' % self.country_name

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('methods', lazy=True))
    #step_number = db.Column(db.Integer)
    method_description = db.Column(Text)

    def __init__(self, method_description, recipe):
        #self.step_number = step_number
        self.method_description = method_description
        self.recipe = recipe
    
    def __repr__(self):
        return '<Method %r>' % self.method_description

class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allergen_name = db.Column(String(150), nullable=False, unique=True)

    def __init__(self, allergen_name):
        self.allergen_name = allergen_name
    
    def __repr__(self):
        return '<Allergen %r>' % self.allergen_name

db.Table('recipe_allergen',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('allergen_id', db.Integer, db.ForeignKey('allergen.id'))
    )

class Dietary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dietary_name = db.Column(String(150), nullable=False, unique=True)

    def __init__(self, dietary_name):
        self.dietary_name = dietary_name
    
    def __repr__(self):
        return '<Dietary %r>' % self.dietary_name

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
    category = db.relationship('Category', backref=db.backref('recipes', lazy=True))
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('recipes', lazy=True))
    
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)
    cuisine = db.relationship('Cuisine', backref=db.backref('recipes', lazy=True))

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('recipes', lazy=True))

    #steps = db.relationship('Step', backref='recipe', lazy='dynamic')
    # quantities = db.relationship('Quantity')
    
    allergens = db.relationship('Allergen', secondary='recipe_allergen', backref='recipe', lazy='dynamic')
    dietaries = db.relationship('Dietary', secondary='recipe_dietary', backref='recipe', lazy='dynamic')

    def __init__(self, recipe_name, recipe_description, preparation_time, cooking_time, servings, category, course, cuisine, author):
        self.recipe_name = recipe_name
        self.recipe_description = recipe_description
        self.preparation_time = preparation_time
        self.cooking_time = cooking_time
        self.servings = servings
        self.category = category
        self.course = course
        self.cuisine = cuisine
        self.author = author

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(String(150), nullable=False, unique=True)

    # quantities = db.relationship('Quantity')

    def __init__(self, ingredient_name):
        self.ingredient_name = ingredient_name
    
    def __repr__(self):
        return '<Ingredient %r>' % self.ingredient_name

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_name = db.Column(String(150), nullable=False, unique=True)

    # quantities = db.relationship('Quantity')

    def __init__(self, measurement_name):
        self.measurement_name = measurement_name
    
    def __repr__(self):
        return '<Measurement %r>' % self.measurement_name


class Quantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('quantities', lazy=True))
    
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    ingredient = db.relationship('Ingredient', backref=db.backref('quantities', lazy=True))
    
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurement.id'), nullable=False)
    measurement = db.relationship('Measurement', backref=db.backref('quantities', lazy=True))

    def __init__(self, quantity, recipe, ingredient, measurement):
        self.quantity = quantity
        self.recipe = recipe
        self.ingredient = ingredient
        self.measurement = measurement
    
    def __repr__(self):
        return '<Quantity %r>' % self.quantity
    
    