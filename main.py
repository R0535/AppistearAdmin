from flask import Flask, request,render_template,session,url_for, flash#request: Contains the self-elements of the request entity
from flask.helpers import make_response          #render_template: the html files manager. secondary parameters managed as cookies render_template("file.html", some_data = some_data)
from werkzeug.utils import redirect              #redirect: to create hubs where can be managed security or other stuff
from wtforms.fields import StringField,PasswordField,SubmitField    #Main input fields to manage the forms <<StringField = Input>> <<PasswordField = Hidden Input>> <<SubmitField = button Input>>
from app.forms import LoginForm
import unittest                                  #imports the testing runner

from app import create_app


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

@app.route('/home')                             #URL decorator with URI name /hello = welcome page
def home():                                     #The def name for the routing behaivour
    user_ip = session.get('user_ip')     #cookie client ip called from the cookie setted in line <<response.set_cookie(user_ip . . .)>>
    username = session.get('username')             #session client name called from the session[data] setted in line <<session['user_ip'] = user_ip . . .>>
    context = {                                  #Dictionary for the main app-data
        "username": username,
        "todos": todos,
        "user_ip":user_ip,
    }

    return render_template('home.html',**context) #returned the response to the client. This time, with the html page



