from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask import render_template, redirect, url_for, request, jsonify
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os, sys

# create an instance of flask = app variable
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://kysizwusmalerj:34940a84c506261a35979f764de8bf76b8d685213c52691ab175e4ef8f7613b2@ec2-54-83-59-120.compute-1.amazonaws.com:5432/dd373to8dgntk1"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# grab the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

# Uploads
app.config['UPLOADS_DEFAULT_DEST'] = TOP_LEVEL_DIR + '/static/img/'
app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/static/img/'
 
app.config['UPLOADED_IMAGES_DEST'] = TOP_LEVEL_DIR + '/static/img/'
app.config['UPLOADED_IMAGES_URL'] = 'http://localhost:5000/static/img/'

# get heroku environment variables and pass them to flask
heroku = Heroku(app)

#app.config.from_pyfile('models.py')

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


from models import db, Recipe, Category, Course, Cuisine, Country, Allergen, Dietary, Author, Measurement, Quantity, Ingredient, Method

#############################INDEX##########################################
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/get_recipes')
def get_recipes_json():
    # recipes = {}
    recipes = []
    for r in db.session.query(Recipe).all():
        print(r, file=sys.stdout)
        # recipies[r.id] = {
        #     'recipe_name': r.recipe_name,
        #     'recipe_description': r.recipe_description,
        #     'category': r.category.category_name,
        #     'cuisine': r.cuisine.cuisine_name,
        #     'course': r.course.course_name,
        #     'author': r.author.author_name
        # }
        recipes.append({
            'recipe_name': r.recipe_name,
            'recipe_description': r.recipe_description,
            'category': r.category.category_name,
            'cuisine': r.cuisine.cuisine_name,
            'course': r.course.course_name,
            'author': r.author.author_name
        })


    return jsonify(recipes)

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

            filename = images.save(request.files['recipe_image'])
            url = images.url(filename)

            recipe = Recipe(request.form['recipe_name'], 
            request.form['recipe_description'], 
            request.form['preparation_time'], 
            request.form['cooking_time'], 
            request.form['servings'],
            recipe_category,
            recipe_course,
            recipe_cuisine,
            recipe_author,
            filename,
            url)

            db.session.add(recipe)

            db.session.commit()
            return redirect(url_for('recipe_list'))
        
        return render_template('add_recipe.html', categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

@app.route('/edit_recipe/<id>')
def edit_recipe(id):
        recipe = Recipe.query.get(id)
        categories_list = Category.query.limit(100).all()
        courses_list = Course.query.limit(100).all()
        cuisines_list = Cuisine.query.limit(100).all()
        authors_list = Author.query.limit(100).all()
        return render_template('edit_recipe.html', recipe=recipe, categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

@app.route('/update_recipe/<id>', methods = ['GET','POST'])
def update_recipe(id):
        
        if request.method == 'POST':
            recipe = Recipe.query.get(id)

            filename = images.save(request.files['recipe_image'])
            url = images.url(filename)

            recipe.recipe_name = request.form['recipe_name']
            recipe.recipe_description = request.form['recipe_description']
            recipe.preparation_time = request.form['preparation_time']
            recipe.cooking_time = request.form['cooking_time']
            recipe.servings = request.form['servings']
            recipe.recipe_category = Category.query.filter_by(id=request.form['recipe_category']).first()
            recipe.recipe_course = Course.query.filter_by(id=request.form['recipe_course']).first()
            recipe.recipe_cuisine = Cuisine.query.filter_by(id=request.form['recipe_cuisine']).first()
            recipe.recipe_author = Author.query.filter_by(id=request.form['recipe_author']).first()
            recipe.image_filename = filename
            recipe.image_url = url

            db.session.commit()
            return redirect(url_for('recipe_list'))
        
        return redirect(url_for('recipe_list'))

@app.route('/delete_recipe/<id>')
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipe_list'))

#############################ADD INGREDIENT##########################################
@app.route('/add_quantity/<id>', methods = ['GET','POST'])
def add_quantity(id):
        measurements_list = Measurement.query.limit(100).all()
        # ingredients_list = Ingredient.query.limit(500).all()
        quantity_recipe = Recipe.query.get(id)
        
        if request.method == 'POST':
            # recipe = Recipe.query.filter_by(id=int(id)).first()
            
            # quantity_recipe = Recipe.query.filter_by(id=recipe.id).first()
            quantity_measurement = Measurement.query.filter_by(id=request.form['quantity_measurement']).first()
            # quantity_ingredient = Ingredient.query.filter_by(id=request.form['quantity_ingredient']).first()
            quantity_ingredient = Ingredient(request.form['quantity_ingredient'])

            quantity = Quantity(request.form['quantity'], 
            quantity_recipe, 
            quantity_ingredient, 
            quantity_measurement)

            db.session.add(quantity)

            db.session.commit()
            return redirect(url_for('recipe_detail', id=id))
        
        return render_template('add_quantity.html', measurements_list=measurements_list, recipe=quantity_recipe)

@app.route('/edit_quantity/<id>')
def edit_quantity(id):
        quantity = Quantity.query.get(id)
        quantity_recipe = Recipe.query.get(quantity.recipe_id)
        # ingredients_list = Ingredient.query.limit(500).all()
        measurements_list = Measurement.query.limit(100).all()
        return render_template('edit_quantity.html', quantity=quantity, measurements_list=measurements_list, recipe=quantity_recipe)

@app.route('/update_quantity/<id>', methods = ['GET','POST'])
def update_quantity(id):
        quantity = Quantity.query.get(id)
        quantity_recipe = Recipe.query.get(quantity.recipe_id)
        # ingredients_list = Ingredient.query.limit(500).all()
        measurements_list = Measurement.query.limit(100).all()
        
        
        if request.method == 'POST':
            quantity = Quantity.query.get(id)

            quantity.quantity = request.form['quantity']
            quantity.recipe = quantity_recipe
            quantity.measurement = Measurement.query.filter_by(id=request.form['quantity_measurement']).first()
            # quantity.ingredient = Ingredient.query.filter_by(id=request.form['quantity_ingredient']).first()
            quantity.ingredient = request.form['quantity_ingredient']


            db.session.commit()
            return redirect(url_for('recipe_detail', id=quantity_recipe.id))
        
        return redirect(url_for('recipe_detail', id=quantity_recipe.id))

@app.route('/delete_quantity/<id>')
def delete_quantity(id):
    quantity = Quantity.query.get(id)
    quantity_recipe = Recipe.query.get(quantity.recipe_id)
    db.session.delete(quantity)
    db.session.commit()
    return redirect(url_for('recipe_detail', id=quantity_recipe.id))

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

@app.route('/edit_method/<id>')
def edit_method(id):
        method = Method.query.get(id)
        method_recipe = Recipe.query.get(method.recipe_id)
        return render_template('edit_method.html', method=method, recipe=method_recipe)

@app.route('/update_method/<id>', methods = ['GET','POST'])
def update_method(id):
        method = Method.query.get(id)
        method_recipe = Recipe.query.get(method.recipe_id)
        
        
        if request.method == 'POST':
            method = Method.query.get(id)

            method.method_description = request.form['method']
            method.recipe = method_recipe

            db.session.commit()
            return redirect(url_for('recipe_detail', id=method_recipe.id))
        
        return redirect(url_for('recipe_detail', id=method_recipe.id))

@app.route('/delete_method/<id>')
def delete_method(id):
    method = Method.query.get(id)
    method_recipe = Recipe.query.get(method.recipe_id)
    db.session.delete(method)
    db.session.commit()
    return redirect(url_for('recipe_detail', id=method_recipe.id))

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

@app.route('/edit_category/<id>')
def edit_category(id):
    category = Category.query.get(id)
    return render_template('edit_category.html', category=category)

@app.route('/update_category/<id>', methods = ['POST'])
def update_category(id):
    category = Category.query.get(id)
    category.category_name = request.form['category']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_category/<id>')
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################COURSE##########################################
@app.route('/add_course', methods = ['POST'])
def add_course():
    course = Course(request.form['course'])
    db.session.add(course)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_course/<id>')
def edit_course(id):
    course = Course.query.get(id)
    return render_template('edit_course.html', course=course)

@app.route('/update_course/<id>', methods = ['POST'])
def update_course(id):
    course = Course.query.get(id)
    course.course_name = request.form['course']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_course/<id>')
def delete_course(id):
    course = Course.query.get(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################CUISINE##########################################
@app.route('/add_cuisine', methods = ['POST'])
def add_cuisine():
    cuisine = Cuisine(request.form['cuisine'])
    db.session.add(cuisine)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_cuisine/<id>')
def edit_cuisine(id):
    cuisine = Cuisine.query.get(id)
    return render_template('edit_cuisine.html', cuisine=cuisine)

@app.route('/update_cuisine/<id>', methods = ['POST'])
def update_cuisine(id):
    cuisine = Cuisine.query.get(id)
    cuisine.cuisine_name = request.form['cuisine']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_cuisine/<id>')
def delete_cuisine(id):
    cuisine = Cuisine.query.get(id)
    db.session.delete(cuisine)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################COUNTRY##########################################
@app.route('/add_country', methods = ['POST'])
def add_country():
    country = Country(request.form['country'])
    db.session.add(country)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_country/<id>')
def edit_country(id):
    country = Country.query.get(id)
    return render_template('edit_country.html', country=country)

@app.route('/update_country/<id>', methods = ['POST'])
def update_country(id):
    country = Country.query.get(id)
    country.country_name = request.form['country']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_country/<id>')
def delete_country(id):
    country = Country.query.get(id)
    db.session.delete(country)
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

@app.route('/edit_author/<id>')
def edit_author(id):
    author = Author.query.get(id)
    countries_list = Country.query.limit(250).all()
    return render_template('edit_author.html', author=author, countries_list=countries_list)

@app.route('/update_author/<id>', methods = ['POST'])
def update_author(id):
    author = Author.query.get(id)
    author.author_name = request.form['author']
    author.country = Country.query.filter_by(id=request.form['author_country']).first()
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_author/<id>')
def delete_author(id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################ALLERGEN##########################################
@app.route('/add_allergen', methods = ['POST'])
def add_allergen():
    allergen = Allergen(request.form['allergen'])
    db.session.add(allergen)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_allergen/<id>')
def edit_allergen(id):
    allergen = Allergen.query.get(id)
    return render_template('edit_allergen.html', allergen=allergen)

@app.route('/update_allergen/<id>', methods = ['POST'])
def update_allergen(id):
    allergen = Allergen.query.get(id)
    allergen.allergen_name = request.form['allergen']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_allergen/<id>')
def delete_allergen(id):
    allergen = Allergen.query.get(id)
    db.session.delete(allergen)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################DIETARY##########################################
@app.route('/add_dietary', methods = ['POST'])
def add_dietary():
    dietary = Dietary(request.form['dietary'])
    db.session.add(dietary)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_dietary/<id>')
def edit_dietary(id):
    dietary = Dietary.query.get(id)
    return render_template('edit_dietary.html', dietary=dietary)

@app.route('/update_dietary/<id>', methods = ['POST'])
def update_dietary(id):
    dietary = Dietary.query.get(id)
    dietary.dietary_name = request.form['dietary']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_dietary/<id>')
def delete_dietary(id):
    dietary = Dietary.query.get(id)
    db.session.delete(dietary)
    db.session.commit()
    return redirect(url_for('manage_static_data'))
#############################MEASUREMENT##########################################
@app.route('/add_measurement', methods = ['POST'])
def add_measurement():
    measurement = Measurement(request.form['measurement'])
    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_measurement/<id>')
def edit_measurement(id):
    measurement = Measurement.query.get(id)
    return render_template('edit_measurement.html', measurement=measurement)

@app.route('/update_measurement/<id>', methods = ['POST'])
def update_measurement(id):
    measurement = Measurement.query.get(id)
    measurement.measurement_name = request.form['measurement']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_measurement/<id>')
def delete_measurement(id):
    measurement = Measurement.query.get(id)
    db.session.delete(measurement)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################INGREDIENT##########################################
@app.route('/add_ingredient', methods = ['POST'])
def add_ingredient():
    ingredient = Ingredient(request.form['ingredient'])
    db.session.add(ingredient)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/edit_ingredient/<id>')
def edit_ingredient(id):
    ingredient = Ingredient.query.get(id)
    return render_template('edit_ingredient.html', ingredient=ingredient)

@app.route('/update_ingredient/<id>', methods = ['POST'])
def update_ingredient(id):
    ingredient = Ingredient.query.get(id)
    ingredient.ingredient_name = request.form['ingredient']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/delete_ingredient/<id>')
def delete_ingredient(id):
    ingredient = Ingredient.query.get(id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

if __name__ == '__main__':
    app.run()