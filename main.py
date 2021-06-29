from flask import Flask, request,render_template,session,url_for, flash #request: Contains the self-elements of the request entity
from flask.helpers import make_response                                 #render_template: the html files manager. secondary parameters managed as cookies render_template("file.html", some_data = some_data)
from werkzeug.utils import redirect                                     #redirect: to create hubs where can be managed security or other stuff
from wtforms.fields import StringField,PasswordField,SubmitField        #Main input fields to manage the forms <<StringField = Input>> <<PasswordField = Hidden Input>> <<SubmitField = button Input>>
from app.forms import LoginForm, TaskForm, DeleteTaskForm,UpdateTaskForm
import unittest                                  #imports the testing runner

from flask_login import login_required, current_user
from app import create_app
from app.firestore_service import get_tasks, get_user, get_proyects,create_alumn_task,delete_task,update_task

app =  create_app()       #Inits the FLASK app from app capsule 
todos = ['TODO1','TODO2','TODO3','TODO4']
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
@app.route("/")                                  #URL decorator with URI name / = root   
def index():                                     #The def name for the routing behaivour
    response = make_response(redirect("/auth/login")) #Building a response manually. Redirecting to other URI behaivour
    return response                              #returned the response to the client. 

@app.route('/home',methods = ['GET','POST'])                             #URL decorator with URI name /hello = welcome page
@login_required                                 #Auth decorator: redirects to login if session is not found
def home():                                     #home manager function
    delete_form = DeleteTaskForm()
    update_form = UpdateTaskForm()
    user_id = session.get('user_id')
    user = get_user(user_id)
    username = user.to_dict()['username']
    user_ip = session.get('user_ip')     #cookie client ip called from the cookie setted in line <<response.set_cookie(user_ip . . .)>>
    task_form = TaskForm()
    projects = get_proyects(user_id)
    project = projects[0]
    tasks = get_tasks(user.id,project.id)
    for task in tasks:
        print(task.to_dict())
    context = {                                   #Dictionary for the main app-data
        "username": username,
        "todos": get_tasks(user.id,project.id),
        "user_ip":user_ip,
        "task_form": task_form,
        "delete_form": delete_form,
        "update_form": update_form,
    }
    if task_form.validate_on_submit():
        create_alumn_task(user_id,project.id,task_form)
        flash("Submited form")
        return redirect(url_for('home'))
    return render_template('home.html',**context) #returned the response to the client. This time, with the html page

@app.route('/tasks/delete/<task_id>',methods = ['POST'])
def delete(task_id):
    user_id = current_user.id
    projects = get_proyects(user_id)
    project = projects[0]
    delete_task(user_id,project.id,task_id)
    return redirect(url_for('home'))

@app.route('/tasks/update/<task_id>/<int:done>',methods = ['POST'])
def update(task_id,done):
    user_id = current_user.id
    projects = get_proyects(user_id)
    project = projects[0]
    update_task(user_id,project.id,task_id,done)
    return redirect(url_for('home'))

