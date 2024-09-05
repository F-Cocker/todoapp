from . import db
from datetime import datetime
#"from . import db" imports the db variable from the parent folder - this is why db is defined before __init__ tries to import this file
#the Todo class is defined to hold all the information we need to build each item in the to-do list
class Todo(db.Model):
    #the ID is set as the primary key as this is what we use to look up specific todo objects
    id=db.Column(db.Integer, primary_key=True)
    #the task is given a character limit and set as unique as this is what the user inputs- the limit and unique requirement help in error handling
    task=db.Column(db.String(300), unique=True)
    #complete is a boolean as it is only ever going to be True or False, this makes it easy to toggle
    complete=db.Column(db.Boolean, default=False)
    #date is when the task was created, it is automatically generated using datetime as imported above
    date=db.Column(db.String, default=datetime.now().strftime("%H:%M %d/%b/%y"))
    #completed_date is set when the complete value is toggled to True. by default, it is blank
    completed_date=db.Column(db.String, default="")