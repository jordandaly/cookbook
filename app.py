from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask import render_template, redirect, url_for, request

# create an instance of flask = app variable
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://kysizwusmalerj:34940a84c506261a35979f764de8bf76b8d685213c52691ab175e4ef8f7613b2@ec2-54-83-59-120.compute-1.amazonaws.com:5432/dd373to8dgntk1"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# get heroku environment variables and pass them to flask
heroku = Heroku(app)

#app.config.from_pyfile('models.py')

from models import db, Recipe, Category, Course, Cuisine, Country, Allergen, Dietary

#############################HOME PAGE##########################################
@app.route('/')
def index():
    recipe_count = Recipe.query.count()
    recipes_list = Recipe.query.limit(100).all()
    return render_template('index.html', recipe_count=str(recipe_count), recipes_list=recipes_list)

# @app.route('/add_recipe', methods = ['GET','POST'])
# def add_recipe():
#     recipe = Recipe(request.form['recipe_name'])
#     db.session.add(category)
#     db.session.commit()
#     return redirect(url_for('index'))

#############################MANAGE STATIC DATA##########################################
@app.route('/manage_static_data')
def manage_static_data():
    category_count = Category.query.count()
    categories_list = Category.query.limit(100).all()

    course_count = Course.query.count()
    courses_list = Course.query.limit(100).all()

    cuisine_count = Cuisine.query.count()
    cuisines_list = Cuisine.query.limit(100).all()

    country_count = Country.query.count()
    countries_list = Country.query.limit(250).all()

    allergen_count = Allergen.query.count()
    allergens_list = Allergen.query.limit(100).all()

    dietary_count = Dietary.query.count()
    dietaries_list = Dietary.query.limit(100).all()
    return render_template('manage_static_data.html', category_count=str(category_count), categories_list=categories_list, course_count=str(course_count), courses_list=courses_list, cuisine_count=str(cuisine_count), cuisines_list=cuisines_list, country_count=str(country_count), countries_list=countries_list, allergen_count=str(allergen_count), allergens_list=allergens_list, dietary_count=str(dietary_count), dietaries_list=dietaries_list)

#############################CATEGORY##########################################
@app.route('/add_category', methods = ['POST'])
def add_category():
    category = Category(request.form['category'])
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################COURSE##########################################
@app.route('/add_course', methods = ['POST'])
def add_course():
    course = Course(request.form['course'])
    db.session.add(course)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################CUISINE##########################################
@app.route('/add_cuisine', methods = ['POST'])
def add_cuisine():
    cuisine = Cuisine(request.form['cuisine'])
    db.session.add(cuisine)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################COUNTRY##########################################
@app.route('/add_country', methods = ['POST'])
def add_country():
    country = Country(request.form['country'])
    db.session.add(country)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################ALLERGEN##########################################
@app.route('/add_allergen', methods = ['POST'])
def add_allergen():
    allergen = Allergen(request.form['allergen'])
    db.session.add(allergen)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################DIETARY##########################################
@app.route('/add_dietary', methods = ['POST'])
def add_dietary():
    dietary = Dietary(request.form['dietary'])
    db.session.add(dietary)
    db.session.commit()
    return redirect(url_for('manage_static_data'))


if __name__ == '__main__':
    app.run()