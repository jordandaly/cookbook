import os
import unittest
 
from app import app, db, BASEDIR
from models import User, Recipe, Category, Course, Cuisine, Author, Country, Measurement, Quantity, Ingredient, Method
 
 
class TestCase(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'test.db') 
        app.config['SECRET_KEY'] = 'secret key'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
 
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    

    ########################
    #### helper methods ####
    ########################

    def register(self, username, password, password2):
        return self.app.post(
            '/register',
            data=dict(username=username, password=password, password2=password2),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')

    def register_user2(self):
        self.app.get('/register', follow_redirects=True)
        self.register('user2@email.com', 'FlaskIsGood', 'FlaskIsGood')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('user@email.com', 'FlaskIsAmazing')

    def login_user2(self):
        self.app.get('/login', follow_redirects=True)
        self.login('user2@email.com', 'FlaskIsGood') 

    def add_static_data(self):
        with app.app_context():
            category1 = Category('Test Category 1')
            category2 = Category('Test Category 2')
            db.session.add(category1)
            db.session.add(category2)
            course1 = Course('Test Course 1')
            course2 = Course('Test Course 2')
            db.session.add(course1)
            db.session.add(course2)
            cuisine1 = Cuisine('Test Cuisine 1')
            cuisine2 = Cuisine('Test Cuisine 2')
            db.session.add(cuisine1)
            db.session.add(cuisine2)
            country1 = Country('Test Country 1')
            country2 = Country('Test Country 2')
            db.session.add(country1)
            db.session.add(country2)
            author_country1 = Country.query.filter_by(country_name='Test Country 1').first()
            author1 = Author('Test Author 1')
            author_country1.authors.append(author1)
            db.session.add(author_country1)
            author_country2 = Country.query.filter_by(country_name='Test Country 2').first()
            author2 = Author('Test Author 2')
            author_country2.authors.append(author2)
            db.session.add(author_country2)
            measurement1 = Measurement('Test Measurement 1')
            measurement2 = Measurement('Test Measurement 2')
            db.session.add(measurement1)
            db.session.add(measurement2)
            ingredient1 = Ingredient('Test Ingredient 1')
            ingredient2 = Ingredient('Test Ingredient 2')
            db.session.add(ingredient1)
            db.session.add(ingredient2)
            db.session.commit()

    def add_test_data(self):
        with app.app_context():
            self.register_user()
            # self.register_user2()
            self.add_static_data()
            user1 = User.query.filter_by(username='user@email.com').first()
            # user2 = User.query.filter_by(username='user2@email.com').first()
            category = Category.query.filter_by(category_name='Test Category 1').first()
            course = Course.query.filter_by(course_name='Test Course 1').first()
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 1').first()
            author = Author.query.filter_by(author_name='Test Author 1').first()
            image_filename = None
            image_url = None
            recipe1 = Recipe(user1, 'Test Recipe Name 1', 'Test Recipe Description 1', 15, 25, 4, category, course, cuisine, author, image_filename, image_url)
            db.session.add(recipe1)
            recipe = Recipe.query.filter_by(recipe_name='Test Recipe Name 1').first()
            measurement = Measurement.query.filter_by(measurement_name='Test Measurement 1').first()
            ingredient = Ingredient.query.filter_by(ingredient_name='Test Ingredient 1').first()
            recipe1_quantity = Quantity(1, recipe, ingredient, measurement)
            db.session.add(recipe1_quantity)
            recipe1_method = Method(recipe, 'Test Method')
            db.session.add(recipe1_method)
            
            # recipe2 = Recipe(user2.id, 'Test Recipe Name 2', 'Test Recipe Description 2', 10, 20, 6, category, course, cuisine, author, image_filename, image_url)
            # db.session.add(recipe2)
            db.session.commit()

 
    ###############
    #### test views ####
    ###############
 
    def test_index_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_my_recipes_page(self):
        response = self.app.get('/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_my_saved_recipes_page(self):
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_manage_categories_page(self):
        response = self.app.get('/manage_static_data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_page(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_page(self):
        response = self.app.get('/add_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ###############
    #### test user auth ####
    ###############
    
    def test_valid_user_registration(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
        #check if user has actually been created
        with app.app_context():
            user = User.query.filter_by(username='user@email.com').first()
            self.assertTrue(user is not None)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsNotAmazing')
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_duplicate_username(self):
        self.register_user()
        response = self.register('user@email.com', 'FlaskIsReallyAmazing', 'FlaskIsReallyAmazing')
        self.assertIn(b'Username already taken, please use a different username.', response.data)

    def test_valid_user_login(self):
        self.register_user()
        response = self.login('user@email.com', 'FlaskIsAmazing')
        self.assertIn(b'Success, you are now logged in!', response.data)

    def test_invalid_user_login_incorrect_username(self):
        self.register_user()
        response = self.login('person@gmail.com', 'FlaskIsAmazing')
        self.assertIn(b'Invalid username', response.data)

    def test_invalid_user_login_incorrect_password(self):
        self.register_user()
        response = self.login('user@email.com', 'FlaskIsOK')
        self.assertIn(b'Invalid password', response.data)

    def test_user_logout(self):
        self.register_user()
        self.login_user()
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout successful', response.data)

    ###############
    #### test CRUD functions####
    ###############

    def test_recipe_list(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)

    def test_recipe_detail(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/recipe_detail/1', follow_redirects=True)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)
        self.assertIn(b'Submitted by: user@email.com', response.data)
        self.assertIn(b'Test Category 1', response.data)
        self.assertIn(b'Test Course 1', response.data)
        self.assertIn(b'Test Cuisine 1', response.data)
        self.assertIn(b'Test Author 1', response.data)
        self.assertIn(b'15 Minutes', response.data)
        self.assertIn(b'25 Minutes', response.data)
        self.assertIn(b'6', response.data)
        self.assertIn(b'1.0 Test Measurement 1 Test Ingredient 1', response.data)
        self.assertIn(b'Test Method', response.data)

    def test_add_recipe(self):
        with app.app_context():
            self.add_static_data()
            category = Category.query.filter_by(category_name='Test Category 1').first()
            course = Course.query.filter_by(course_name='Test Course 1').first()
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 1').first()
            author = Author.query.filter_by(author_name='Test Author 1').first()
            self.register_user()
            self.login_user()
            response = self.app.post('/add_recipe',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': 'Test Recipe Name A',
                                            'recipe_description': 'Test Recipe Description A',
                                            'preparation_time': 30,
                                            'cooking_time': 60,
                                            'servings': 8,
                                            'recipe_category': category.id,
                                            'recipe_course': course.id,
                                            'recipe_cuisine': cuisine.id,
                                            'recipe_author' : author.id
                                            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Recipe Name A', response.data)

    def test_edit_recipe(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/edit_recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Recipe', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)
        self.assertIn(b'Test Category 1', response.data)
        self.assertIn(b'Test Course 1', response.data)
        self.assertIn(b'Test Cuisine 1', response.data)
        self.assertIn(b'Test Author 1', response.data)
        self.assertIn(b'15', response.data)
        self.assertIn(b'25', response.data)
        self.assertIn(b'4', response.data)

    def test_update_recipe(self):
        with app.app_context():
            self.add_test_data()
            category = Category.query.filter_by(category_name='Test Category 2').first()
            course = Course.query.filter_by(course_name='Test Course 2').first()
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 2').first()
            author = Author.query.filter_by(author_name='Test Author 2').first()
            self.login_user()
            response = self.app.post('/update_recipe/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': 'Test Recipe Name 2',
                                            'recipe_description': 'Test Recipe Description 2',
                                            'preparation_time': 16,
                                            'cooking_time': 26,
                                            'servings': 5,
                                            'recipe_category': category.id,
                                            'recipe_course': course.id,
                                            'recipe_cuisine': cuisine.id,
                                            'recipe_author' : author.id
                                            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Recipe Name 2', response.data)
            self.assertIn(b'Test Recipe Description 2', response.data)
            self.assertIn(b'Test Category 2', response.data)
            self.assertIn(b'Test Course 2', response.data)
            self.assertIn(b'Test Cuisine 2', response.data)
            self.assertIn(b'Test Author 2', response.data)
            self.assertIn(b'16 Minutes', response.data)
            self.assertIn(b'26 Minutes', response.data)
            self.assertIn(b'5', response.data)

    def test_delete_recipe(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.get('/delete_recipe/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Test Recipe Name 1', response.data)

    def test_add_quantity(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            measurement = Measurement.query.filter_by(measurement_name='Test Measurement 2').first()
            response = self.app.post('/add_quantity/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'quantity': 2,
                                          'quantity_ingredient': 'Test Ingredient A',
                                          'quantity_measurement': measurement.id
                                          }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'2.0 Test Measurement 2 Test Ingredient A', response.data)

    def test_update_quantity(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            measurement = Measurement.query.filter_by(measurement_name='Test Measurement 2').first()
            response = self.app.post('/update_quantity/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'quantity': 2,
                                          'quantity_ingredient': 'Test Ingredient 1 Updated',
                                          'quantity_measurement': measurement.id
                                          }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'2.0 Test Measurement 2 Test Ingredient 1 Updated', response.data)

 
if __name__ == "__main__":
    unittest.main()