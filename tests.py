import os
import unittest
 
from app import app, db, BASEDIR
from models import User
 
 
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
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')
        self.assertEqual(response.status_code, 200)
        response = self.register('user@email.com', 'FlaskIsReallyAmazing', 'FlaskIsReallyAmazing')
        self.assertIn(b'Username already taken, please use a different username.', response.data)

    def test_valid_user_login(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')
        self.assertEqual(response.status_code, 200)
        response = self.login('user@email.com', 'FlaskIsAmazing')
        self.assertIn(b'Success, you are now logged in!', response.data)

    def test_invalid_user_login_incorrect_username(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')
        self.assertEqual(response.status_code, 200)
        response = self.login('user2@email.com', 'FlaskIsAmazing')
        self.assertIn(b'Invalid username', response.data)

    def test_invalid_user_login_incorrect_password(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')
        self.assertEqual(response.status_code, 200)
        response = self.login('user@email.com', 'FlaskIsOK')
        self.assertIn(b'Invalid password', response.data)

    def test_user_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout successful', response.data)

 
if __name__ == "__main__":
    unittest.main()