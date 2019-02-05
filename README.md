# Cookbook | Flask & PostgreSQL Data Centric Development Project

## UX Design

Details of the UX design is available in the 'DCD project design' folder. This folder contains documents that illustrate the user interface design by way of wireframe mockups of the main web pages of the application.

## Database Design

Details of the Database design is available in the
'Database Schema' folder. The ERD (Entity Relationship Diagram) document outlines how I approached the design of the Database.

## Features

### Existing Features

This is a web application which that allows users to store and easily access cooking recipes. It is a full stack web application (frontend and backend) that provides CRUD (Create, Read, Update, Delete) functionality to a database hosted in the cloud on Heroku platform as a service. Users can :
1.	Recipe Search: search by recipe name, search by ingredient and filter recipes by category, course, cuisine and author on the index page. 
2.	Add Recipe: Add a new recipe and then Add ingredients and methods to the recipe on the recipe detail page.
3.	Manage Categories: Add new and Edit existing static data like categories, courses, cuisines, authors, measurements etc.
4.	My Recipes: view a list of recipes submitted by the current logged in user.
5.  Saved Recipes: view and manage a list of recipes saved by the current logged in user.
6.  Dashboard: displays interactive dashboard of charts; Categories bar chart, courses pie chart, cuisines row chart and author bar chart. 
7. Recipe Detail: Save, Edit and Delete recipes, Edit and Delete ingredients, Edit and Delete methods.

### Features Left to Implement
1. Allergens and Dietary

## Demo

A demo of this web application is available [here](https://daly-cookbook.herokuapp.com/).


## Getting started /

1. Clone the repo and cd into the project directory.
2. Ensure you have Python 3 and Postgres installed and create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`.


## Technologies Used

**HTML, CSS, JavaScript (Front End Framework Materialize)  Python, Full Stack Micro Framework Flask, PostgreSQL an object-relational database management system :**

## Testing

Automated tests were carried out and all 47 tests passed satisfactorily (see screenshot in Testing folder). They are located in the file tests.py and can be ran using the command:
`python3 tests.py`

Manual testing was undertaken for this application and satisfactorily passed. A sample of the tests conducted are as follows:
1.	Testing navigation buttons and hyperlinks throughout the page
2.	Testing the CRUD functionality
3.	Testing the responsiveness of the application on different browsers and then using different devices.

## Deployment
1. Make sure requirements.txt and Procfile exist:
`pip3 freeze --local requirements.txt`
`echo web: python app.py > Procfile`
2. Create Heroku App, Select Postgres add-on, download Heroku CLI toolbelt, login to heroku (Heroku login), git init, connect git to heroku (heroku git remote -a <project>), git add ., git commit, git push heroku master.
3. heroku ps:scale web=1
4. In heroku app settings set the config vars to add DATABASE_URL, IP and PORT

## Credits

**Jordan Daly** - This project was completed as part of Code Institute’s Mentored Online Full Stack Web Development course in 2018.

### Content
The content for recipes was taken from the [BBC recipes website](https://www.bbc.com/food/recipes).

### Media
The images for recipes were also taken from the BBC recipes website.

### Acknowledgements
Image upload to AWS S3 with boto3 info from this [blog](http://zabana.me/notes/upload-files-amazon-s3-flask.html).
Unit testing strategy from this [blog](https://www.patricksoftwareblog.com/unit-testing-a-flask-application/).  
