from flask import Blueprint, redirect, render_template, url_for, request
from datetime import datetime
from .models import Todo
from . import db
#the necessary functions from flask, datetime and models are imported
#"from . import db" imports the db variable from the parent folder - this is why db is defined before __init__ tries to import this file

#the blueprint is set up for the routes to reference
my_view=Blueprint("my_view", __name__)

#index route, simply loads the homepage after loading the list of todos from the database
@my_view.route("/")
def home():
    todo_list=Todo.query.all()
    #error message is requested, if the user was redireted here with no error, it will not dispaly
    error=request.args.get("error", None)
    message=request.args.get("message",None)
    return render_template("index.html", todo_list=todo_list, error=error, message=message)

#the route for adding a new item to the todo list. the POST method is required as this is done via a form
@my_view.route("/add", methods=["POST"])
def add():
    #the user's input is requested from the form
    task=request.form.get("task")
    #the full list of existing todos is grabbed to check for duplicates
    todo_list=Todo.query.all()
    #this for loop iterates through the list and checks if the new task is identical to an existing one
    for todo in todo_list:
        if todo.task==task:
            #if any of the tasks are the same as the input, the user is returned to the page without adding a new task, with an error message
            error="Could not add task: Task already exists"
            return redirect(url_for("my_view.home", error=error))
    #if no duplicates are found, the new item is added to the list. only todo is based on user input, the other data is all generated automatically
    new_todo=Todo(task=task, date=datetime.now().strftime("%H:%M %d/%b/%y"))
    db.session.add(new_todo)
    #commit is necessary to update the database
    db.session.commit()
    #the user is redirected back to the main page with the new todo added
    message="Task added successfully"
    return redirect(url_for("my_view.home", message=message))

#the update route flips the boolean value of "completed" back and forth
@my_view.route("/update/<todo_id>")
def update(todo_id):
    #this line searches the database for the ID given by the website to find the correct todo item
    todo=Todo.query.filter_by(id=todo_id).first()
    #the todo.complete variable is set to "not itself". because it is a boolean, this simply flips it from True to False and vice versa
    todo.complete=not todo.complete
    #if the boolean has been flipped from False to True, the todo.completed_date is updated from a blank space to the current time
    if todo.complete==True:
        todo.completed_date=datetime.now().strftime("%H:%M %d/%b/%y")
    #else, if it was flipped from True to False, the todo.completed_date is set back to blank
    else:
        todo.completed_date=""
    #updated data is commited to database
    db.session.commit()
    #returned to main page with update now displayed
    message="Task updated"
    return redirect(url_for("my_view.home", message=message))

#the delete route removes the specified todo from the list, completely deleting it
@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    #todo is found by searching the ID
    todo=Todo.query.filter_by(id=todo_id).first()
    #the todo is deleted and committed
    db.session.delete(todo)
    db.session.commit()
    message="Task deleted"
    return redirect(url_for("my_view.home", message=message))

#edit changes the name of the todo to a new value set by the user
@my_view.route("/edit/<todo_id>", methods=["POST"])
def edit(todo_id):
    #the data inputted by the user is grabbed from the form
    edit=request.form.get("edit")
    #the todo_list is loaded to check for duplicates
    todo_list=Todo.query.all()
    for todo in todo_list:
        if todo.task==edit:
            #if the edit is a duplicate, the todo is not changed and the user is given an error
            error="Could not edit task: Task already exists"
            return redirect(url_for("my_view.home", error=error))
    #if the edit is not a duplicate, the todo is searched via ID
    todo=Todo.query.filter_by(id=todo_id).first()
    #todo.task is set to the users input with no other data changed, then commited to database
    todo.task=edit
    db.session.commit()
    message="Task edited"
    return redirect(url_for("my_view.home", message=message))