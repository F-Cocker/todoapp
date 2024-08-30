from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#The __init__ file uses the information from views and models to compile all the necessary information
#So that it can be used within the single function to build the app.
#flask and sqlalchemy are imported as they are necessary for the app and database

#db is defined as a database for the website to use
db=SQLAlchemy()

#create_app is defined, first defining app using the default Flask() setup
#The app.config for SQLAlchemy is set so that the database can function
def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
    #database is initialized
    db.init_app(app)
    #The views are imported here, this is done after db is defined as views uses the db variable
    from .views import my_view
    app.register_blueprint(my_view)
    #The Todo class is imported from models, this is again important to be done after db is defined
    from .models import Todo
    with app.app_context():
        db.create_all()
    #Once the app and database are initialized, the app Flask object is retuned to the function called in app.py
    return app