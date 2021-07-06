from flask import Flask, request,render_template,session,url_for, flash #request: Contains the self-elements of the request entity
from flask.helpers import make_response                                 #render_template: the html files manager. secondary parameters managed as cookies render_template("file.html", some_data = some_data)
from werkzeug.utils import redirect                                     #redirect: to create hubs where can be managed security or other stuff
from wtforms.fields import StringField,PasswordField,SubmitField        #Main input fields to manage the forms <<StringField = Input>> <<PasswordField = Hidden Input>> <<SubmitField = button Input>>
from app.forms import LoginForm, TaskForm,UpdateTaskForm

from app.forms import InitialAddForm,InitialSearchForm,InitialRateForm  #Buttons for Home Actions
from app.forms import AddForm  #Forms for ADD, Search and Rate
import unittest                                                         #imports the testing runner

from flask_login import login_required, current_user
from app import create_app
from app.firestore_service import get_tasks, get_user, get_proyects,create_alumn_task,delete_task,update_task

#Google MAPS
import json
from flask_googlemaps import GoogleMaps, Map
from keys import GOOGLE_KEY


app =  create_app()       #Inits the FLASK app from app capsule 
app.config['GOOGLEMAPS_KEY'] = GOOGLE_KEY

#GOOGLE MAPS INFO
GoogleMaps(app)
#Maps Utilities
user_location = (37,127)
circle = { # draw circle on map (user_location as center)
        'stroke_color': '#0000FF',
        'stroke_opacity': .5,
        'stroke_weight': 5,
        # line(stroke) style
        'fill_color': '#FFFFFF', 
        'fill_opacity': .2,
        # fill style
        'center': { # set circle to user_location
            'lat': user_location[0],
            'lng': user_location[1]
        }, 
        'radius': 500 # circle size (50 meters)
    }

@app.cli.command()
# def test():
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner().run(tests)

@app.route("/")                                                          #URL decorator with URI name / = root   
def index():
    session["user_ip"] = request.remote_addr                                                             #The def name for the routing behaivour
    response = make_response(redirect("/home"))                          #Building a response manually. Redirecting to other URI behaivour
    return response                                                      #returned the response to the client. 

@app.route('/home',methods = ['GET','POST'])                             #URL decorator with URI name /hello
def home():                                                              #home manager function
    add_form = InitialAddForm()
    search_form = InitialSearchForm()
    rate_form = InitialRateForm()

    context = {                                   #Dictionary for the HTML part
        "add_form": add_form,
        "search_form": search_form,
        "rate_form": rate_form,
    }
    if add_form.validate_on_submit():
        flash("Nueva Cueva")
        print("AAAAAAAAAAAA")
        return redirect(url_for('add'))
    if search_form.validate_on_submit():
        flash("Nueva Cueva")
        print("AAAAAAAAAAAA")
        return redirect(url_for('add'))
    if rate_form.validate_on_submit():
        flash("Nueva Cueva")
        print("AAAAAAAAAAAA")
        return redirect(url_for('add'))
    return render_template('home.html',**context) #returned the response to the client. This time, with the html page

@app.route('/add',methods = ["GET",'POST'])
def add():
    
    #Create a map
    map = Map(
        identifier = "map", varname = "map",style="height:600px;width:600px;margin:0;",
        # set identifier, varname
        lat = user_location[0], lng = user_location[1], 
        # set map base to user_location
        zoom = 15, # set zoomlevel
        markers = [
            {
                'lat': user_location[0],
                'lng': user_location[1],
                'infobox': "Place"
            }
        ], 
        # set markers to location of devices
        circles = [circle] # pass circles
    )
    add_form = AddForm()
    context = {                                   #Dictionary for the HTML part
        "add_form": add_form,
        "map": map,
        "key":GOOGLE_KEY,
    }
    return render_template('add.html',**context)


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

