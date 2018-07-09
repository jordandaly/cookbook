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



from models import db, Recipe, Category, Course, Cuisine, Country, Allergen, Dietary, Author, Measurement, Quantity, Ingredient, Method

#############################INDEX##########################################
@app.route('/')
def index():
    
    return render_template('index.html')

#############################RECIPE LIST##########################################
@app.route('/recipe_list')
def recipe_list():
    recipe_count = Recipe.query.count()
    recipes_list = Recipe.query.limit(100).all()
    return render_template('recipe_list.html', recipe_count=str(recipe_count), recipes_list=recipes_list)

#############################RECIPE DETAIL##########################################
@app.route('/recipe_detail/<id>')
def recipe_detail(id):

    recipe = Recipe.query.filter_by(id=int(id)).first()

    quantity_list = Quantity.query.filter_by(recipe_id=id)

    method_list = Method.query.filter_by(recipe_id=id)

    return render_template('recipe_detail.html', recipe=recipe, quantity_list=quantity_list, method_list=method_list)

#############################ADD RECIPE##########################################
@app.route('/add_recipe', methods = ['GET','POST'])
def add_recipe():
        categories_list = Category.query.limit(100).all()
        courses_list = Course.query.limit(100).all()
        cuisines_list = Cuisine.query.limit(100).all()
        authors_list = Author.query.limit(100).all()
        
        
        if request.method == 'POST':
            recipe_category = Category.query.filter_by(id=request.form['recipe_category']).first()
            recipe_course = Course.query.filter_by(id=request.form['recipe_course']).first()
            recipe_cuisine = Cuisine.query.filter_by(id=request.form['recipe_cuisine']).first()
            recipe_author = Author.query.filter_by(id=request.form['recipe_author']).first()

            recipe = Recipe(request.form['recipe_name'], 
            request.form['recipe_description'], 
            request.form['preparation_time'], 
            request.form['cooking_time'], 
            request.form['servings'],
            recipe_category,
            recipe_course,
            recipe_cuisine,
            recipe_author)

            db.session.add(recipe)

            db.session.commit()
            return redirect(url_for('recipe_list'))
        
        return render_template('add_recipe.html', categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

#############################ADD INGREDIENT##########################################
@app.route('/add_quantity/<id>', methods = ['GET','POST'])
def add_quantity(id):
        measurements_list = Measurement.query.limit(100).all()
        ingredients_list = Ingredient.query.limit(500).all()
        quantity_recipe = Recipe.query.get(id)
        
        if request.method == 'POST':
            # recipe = Recipe.query.filter_by(id=int(id)).first()
            
            # quantity_recipe = Recipe.query.filter_by(id=recipe.id).first()
            quantity_measurement = Measurement.query.filter_by(id=request.form['quantity_measurement']).first()
            quantity_ingredient = Ingredient.query.filter_by(id=request.form['quantity_ingredient']).first()

            quantity = Quantity(request.form['quantity'], 
            quantity_recipe, 
            quantity_ingredient, 
            quantity_measurement)

            db.session.add(quantity)

            db.session.commit()
            return redirect(url_for('recipe_detail', id=id))
        
        return render_template('add_quantity.html', measurements_list=measurements_list, ingredients_list=ingredients_list, recipe=quantity_recipe)

#############################ADD METHOD##########################################
@app.route('/add_method/<id>', methods = ['GET','POST'])
def add_method(id):       
        method_recipe = Recipe.query.get(id)   
        if request.method == 'POST':
            
            # method_recipe = Recipe.query.filter_by(id=recipe.id).first()

            method = Method(method_recipe,(request.form['method']))

            db.session.add(method)

            db.session.commit()
            return redirect(url_for('recipe_detail', id=id))
        
        return render_template('add_method.html', recipe=method_recipe)

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

    author_count = Author.query.count()
    authors_list = Author.query.limit(100).all()

    allergen_count = Allergen.query.count()
    allergens_list = Allergen.query.limit(100).all()

    dietary_count = Dietary.query.count()
    dietaries_list = Dietary.query.limit(100).all()

    measurement_count = Measurement.query.count()
    measurements_list = Measurement.query.limit(100).all()

    ingredient_count = Ingredient.query.count()
    ingredients_list = Ingredient.query.limit(500).all()
    return render_template('manage_static_data.html', category_count=str(category_count), categories_list=categories_list, course_count=str(course_count), courses_list=courses_list, cuisine_count=str(cuisine_count), cuisines_list=cuisines_list, country_count=str(country_count), countries_list=countries_list, author_count=str(author_count), authors_list=authors_list, allergen_count=str(allergen_count), allergens_list=allergens_list, dietary_count=str(dietary_count), dietaries_list=dietaries_list, measurement_count=str(measurement_count), measurements_list=measurements_list, ingredient_count=ingredient_count, ingredients_list=ingredients_list)

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

#############################AUTHOR##########################################
@app.route('/add_author', methods = ['POST'])
def add_author():
    author_country = Country.query.filter_by(id=request.form['author_country']).first()
    author = Author(request.form['author'])
    author_country.authors.append(author)
    db.session.add(author_country)
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
#############################MEASUREMENT##########################################
@app.route('/add_measurement', methods = ['POST'])
def add_measurement():
    measurement = Measurement(request.form['measurement'])
    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################INGREDIENT##########################################
@app.route('/add_ingredient', methods = ['POST'])
def add_ingredient():
    ingredient = Ingredient(request.form['ingredient'])
    db.session.add(ingredient)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

if __name__ == '__main__':
    app.run()