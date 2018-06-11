from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

# create an instance of flask = app variable
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://kysizwusmalerj:34940a84c506261a35979f764de8bf76b8d685213c52691ab175e4ef8f7613b2@ec2-54-83-59-120.compute-1.amazonaws.com:5432/dd373to8dgntk1"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# get heroku environment variables and pass them to flask
heroku = Heroku(app)

#app.config.from_pyfile('models.py')

from models import db




if __name__ == '__main__':
    app.run()