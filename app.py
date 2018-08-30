from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_heroku import Heroku
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os, sys
from extensions import db, migrate, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from models import User
from forms import RegistrationForm, LoginForm

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

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# get heroku environment variables and pass them to flask
# heroku = Heroku(app)

#app.config.from_pyfile('models.py')

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

login_manager.login_view = 'login'

from models import Recipe, Category, Course, Cuisine, Country, Allergen, Dietary, Author, Measurement, Quantity, Ingredient, Method, User, SavedRecipe


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Congratulations, you are now logged in!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#############################INDEX##########################################
@app.route('/')
def index():
    
    return render_template('index.html')
#############################RECIPE JSON DATA ENDPOINT##########################################
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
@login_required
def recipe_list():
    recipe_count = Recipe.query.count()
    # recipes_list = Recipe.query.limit(100).all()
    page = request.args.get('page', 1, type=int)
    recipes_list = Recipe.query.order_by(Recipe.id.desc()).paginate(page, 10, False)
    next_url = url_for('recipe_list', page=recipes_list.next_num) \
        if recipes_list.has_next else None
    prev_url = url_for('recipe_list', page=recipes_list.prev_num) \
        if recipes_list.has_prev else None
    return render_template('recipe_list.html', recipe_count=str(recipe_count), recipes_list=recipes_list.items, next_url=next_url, prev_url=prev_url)

#############################RECIPE LIST##########################################
@app.route('/my_recipes')
@login_required
def my_recipes():
    recipe_count = Recipe.query.filter_by(user=current_user).count()
    # recipes_list = Recipe.query.limit(100).all()
    page = request.args.get('page', 1, type=int)
    recipes_list = Recipe.query.filter_by(user=current_user).order_by(Recipe.id.desc()).paginate(page, 10, False)
    next_url = url_for('recipe_list', page=recipes_list.next_num) \
        if recipes_list.has_next else None
    prev_url = url_for('recipe_list', page=recipes_list.prev_num) \
        if recipes_list.has_prev else None
    return render_template('my_recipes.html', recipe_count=str(recipe_count), recipes_list=recipes_list.items, next_url=next_url, prev_url=prev_url)

#############################RECIPE LIST FILTERED##########################################
@app.route('/recipe_list_filtered', methods = ['GET','POST'])
@login_required
def recipe_list_filtered():
    categories_list = Category.query.limit(100).all()
    courses_list = Course.query.limit(100).all()
    cuisines_list = Cuisine.query.limit(100).all()
    authors_list = Author.query.limit(100).all()
    
    if request.method == 'POST':
        recipe_category = Category.query.filter_by(id=request.form.get('recipe_category')).first()
        recipe_course = Course.query.filter_by(id=request.form.get('recipe_course')).first()
        recipe_cuisine = Cuisine.query.filter_by(id=request.form.get('recipe_cuisine')).first()
        recipe_author = Author.query.filter_by(id=request.form.get('recipe_author')).first()
        queries = []
        if recipe_category is not None:
            queries.append(Recipe.category == recipe_category)
        if recipe_course is not None:
            queries.append(Recipe.course == recipe_course)
        if recipe_cuisine is not None:
            queries.append(Recipe.cuisine == recipe_cuisine)
        if recipe_author is not None:
            queries.append(Recipe.author == recipe_author)
        
        recipes_list = Recipe.query.filter(*queries).all()
        recipe_count = Recipe.query.filter(*queries).count()
        # recipes_list = Recipe.query.filter_by(category=recipe_category, course=recipe_course, cuisine=recipe_cuisine, author=recipe_author).all()
        # recipe_count = Recipe.query.filter_by(category=recipe_category, course=recipe_course, cuisine=recipe_cuisine, author=recipe_author).count()
        return render_template('recipe_list_filtered.html', recipe_count=str(recipe_count), recipes_list=recipes_list, categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)
    return render_template('recipe_list_filtered.html', categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

#############################RECIPE SEARCH##########################################
@app.route('/recipe_search', methods = ['GET','POST'])
@login_required
def recipe_search():

    
    if request.method == 'POST':
        # kwargs = {'recipe_name': request.form['recipe_name']}
        
        recipes_list = Recipe.query.filter(Recipe.recipe_name.ilike("%" + request.form['recipe_name'] + "%")).all()
        recipe_count = Recipe.query.filter(Recipe.recipe_name.ilike("%" + request.form['recipe_name'] + "%")).count()
        return render_template('recipe_search.html', recipe_count=str(recipe_count), recipes_list=recipes_list)
    return render_template('recipe_search.html')


#############################INGREDIENT SEARCH##########################################
@app.route('/ingredient_search', methods=['GET', 'POST'])
@login_required
def ingredient_search():
    if request.method == 'POST':
        # kwargs = {'recipe_name': request.form['recipe_name']}

        # recipes_list = Recipe.query.filter(Recipe.recipe_name.ilike("%" + request.form['recipe_name'] + "%")).all()
        # recipe_count = Recipe.query.filter(Recipe.recipe_name.ilike("%" + request.form['recipe_name'] + "%")).count()
        recipes = []

        quantity_list = Quantity.query.filter(Quantity.ingredient.has(Ingredient.ingredient_name.ilike("%" + request.form['ingredient_name'] + "%"))).all()
        for quantity in quantity_list:
            recipe_id = quantity.recipe_id
            recipes.append(recipe_id)

        recipes_list = Recipe.query.join(Quantity).filter(Recipe.id.in_(recipes)).all()
        recipe_count = Quantity.query.filter(Quantity.ingredient.has(Ingredient.ingredient_name.ilike("%" + request.form['ingredient_name'] + "%"))).count()
        return render_template('ingredient_search.html', recipe_count=str(recipe_count), recipes_list=recipes_list)
    return render_template('ingredient_search.html')


#############################RECIPE DETAIL##########################################
@app.route('/recipe_detail/<id>')
@login_required
def recipe_detail(id):

    recipe = Recipe.query.filter_by(id=int(id)).first()

    quantity_list = Quantity.query.filter_by(recipe_id=id)

    method_list = Method.query.filter_by(recipe_id=id)

    return render_template('recipe_detail.html', recipe=recipe, quantity_list=quantity_list, method_list=method_list)

#############################RECIPE##########################################
@app.route('/add_recipe', methods = ['GET','POST'])
@login_required
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

            if 'recipe_image' in request.files:
                filename = images.save(request.files['recipe_image'])
                url = images.url(filename)
            else:
                filename = None
                url = None

            recipe = Recipe(current_user,
            request.form['recipe_name'],
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
@login_required
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

            if 'recipe_image' in request.files:
                filename = images.save(request.files['recipe_image'])
                url = images.url(filename)
            else:
                filename = None
                url = None

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
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipe_list'))

#############################INGREDIENT##########################################
@app.route('/add_quantity/<id>', methods = ['GET','POST'])
@login_required
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
@login_required
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
@login_required
def delete_quantity(id):
    quantity = Quantity.query.get(id)
    quantity_recipe = Recipe.query.get(quantity.recipe_id)
    db.session.delete(quantity)
    db.session.commit()
    return redirect(url_for('recipe_detail', id=quantity_recipe.id))

#############################METHOD##########################################
@app.route('/add_method/<id>', methods = ['GET','POST'])
@login_required
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
@login_required
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
@login_required
def delete_method(id):
    method = Method.query.get(id)
    method_recipe = Recipe.query.get(method.recipe_id)
    db.session.delete(method)
    db.session.commit()
    return redirect(url_for('recipe_detail', id=method_recipe.id))

#############################SAVEDRECIPE##########################################
@app.route('/save_recipe/<id>')
@login_required
def save_recipe(id):
    recipe = Recipe.query.get(id)
    existing_saved_recipe = SavedRecipe.query.filter_by(user=current_user, recipe=recipe).first()
    if existing_saved_recipe is None:
        savedrecipe = SavedRecipe(current_user, recipe)
        db.session.add(savedrecipe)
        db.session.commit()
        flash('Recipe added to My Saved Recipes')
    else:
        flash('Recipe already added to My Saved Recipes')
    return redirect(url_for('recipe_detail', id=id))

@app.route('/delete_saved_recipe/<id>')
@login_required
def delete_saved_recipe(id):
    savedrecipe = SavedRecipe.query.get(id)
    db.session.delete(savedrecipe)
    db.session.commit()
    flash('Recipe deleted from My Saved Recipes')
    return redirect(url_for('my_saved_recipes'))

@app.route('/my_saved_recipes')
@login_required
def my_saved_recipes():
    recipe_count = SavedRecipe.query.filter_by(user=current_user).count()
    # recipes_list = Recipe.query.limit(100).all()
    page = request.args.get('page', 1, type=int)
    recipes_list = SavedRecipe.query.filter_by(user=current_user).order_by(SavedRecipe.id.desc()).paginate(page, 10, False)
    next_url = url_for('recipe_list', page=recipes_list.next_num) \
        if recipes_list.has_next else None
    prev_url = url_for('recipe_list', page=recipes_list.prev_num) \
        if recipes_list.has_prev else None
    return render_template('my_saved_recipes.html', recipe_count=str(recipe_count), recipes_list=recipes_list.items, next_url=next_url, prev_url=prev_url)

#############################MANAGE STATIC DATA##########################################
@app.route('/manage_static_data')
@login_required
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)