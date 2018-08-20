# Cookbook | Flask & PostgreSQL Data Centric Development Project

## UX Design

Details of the UX design is available in the 'DCD project design' folder. This document outlines how I approached the design of this site.

## Database Design

Details of the Database design is available in the
'Database Schema' folder. This document outlines how I approached the design of the Database.

## Features

### Existing Features

This is a web application which that allows users to store and easily access cooking recipes. It is a full stack web application (frontend and backend) that provides CRUD (Create, Read, Update, Delete) functionality to a database hosted in the cloud on Heroku platform as a service. Users can :
1.	View a list of recipes, filter list, search by recipe name, search by ingredient
2.	Add a new recipe and add ingredients and method to the recipe
3.	Manage static data like categories
4.	Edit and Delete any data

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

Manual testing was undertaken for this application and satisfactorily passed. A sample of the tests conducted are as follows:
1.	Testing navigation buttons and hyperlinks throughout the page
2.	Testing the CRUD functionality
3.	Testing the responsiveness of the application on different browsers and then using different devices.

## Deployment
1. Make sure requirements.txt and Procfile exist
⋅⋅* pip3 freeze --local requirements.txt
⋅⋅* echo web: python app.py > Procfile
2. Create Heroku App, Select Postgres add-on, download Heroku CLI toolbelt, login to heroku (Heroku login), git init, connect git to heroku (heroku git remote -a <project>), git add ., git commit, git push heroku master.
3. heroku ps:scale web=1
4. In heroku app settings set the config vars to add DATABASE_URL, IP and PORT

## Credits

**Jordan Daly** - This project was completed as part of Code Institute’s Mentored Online Full Stack Web Development course in 2018.

### Content

### Media

### Acknowledgements
