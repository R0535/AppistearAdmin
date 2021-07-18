from flask import Flask, request,render_template,session,url_for, flash #request: Contains the self-elements of the request entity
from flask.helpers import make_response                                 #render_template: the html files manager. secondary parameters managed as cookies render_template("file.html", some_data = some_data)
from werkzeug.utils import redirect                                     #redirect: to create hubs where can be managed security or other stuff
from wtforms.fields import StringField,PasswordField,SubmitField        #Main input fields to manage the forms <<StringField = Input>> <<PasswordField = Hidden Input>> <<SubmitField = button Input>>
from app.forms import LoginForm, TaskForm,UpdateTaskForm

from app.forms import InitialAddForm,InitialSearchForm,InitialRateForm  #Buttons for Home Actions
from app.forms import AddForm ,SearchForm, RateForm  #Forms for ADD, Search and Rate
import unittest                                                         #imports the testing runner

from flask_login import login_required, current_user
from app import create_app
from app.firestore_service import get_places,create_search,get_tasks, get_user, get_proyects,create_alumn_task,delete_task,update_task,create_place

#Google MAPS
import json
from keys import GOOGLE_KEY

#Query and Sort
from app.utilities.query import sort_places
#Data
from datetime import datetime
ADD_QUESTION = "app/static/forms/add.json"
SEARCH_QUESTION = "app/static/forms/search.json"
RATE_QUESTION = "app/static/forms/rate.json"

app = create_app()       #Inits the FLASK app from app capsule 
app.config['GOOGLEMAPS_KEY'] = GOOGLE_KEY


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
        return redirect(url_for('add'))
    if search_form.validate_on_submit():
        flash("Nueva Cueva")
        return redirect(url_for('add'))
    if rate_form.validate_on_submit():
        flash("Nueva Cueva")
        return redirect(url_for('add'))
    return render_template('home.html',**context) #returned the response to the client. This time, with the html page

#Function manager to save the drinking places from the owners info
@app.route('/add',methods = ["GET",'POST'])
def add():
    #Render response
    #reading static file of questions to inject into questions
    questions = None
    with open(ADD_QUESTION,"r",encoding='utf-8') as f:
        data = json.loads(f.read())
        questions = data.get("create")

    #single from
    add_form = AddForm()

    #answers to manage responses
    answers = session.get("answers")#get from cookies the json
    if(answers is None):
        answers = [None]*len(questions)

    coords = questions[1].get("options")
    if(answers[1]):
        coords = answers[1].get("value")

    list2 = []
    for answer in answers:
        if answer:
            answer = answer.get("value")
            list2.append(answer)
        else:
            list2.append(None)
    answers = list2
    context = {#Dictionary for the HTML page
        "key":GOOGLE_KEY,
        "add_form":add_form,
        "questions":questions,
        "answers":answers,
        "coords":coords,
    }
    resp = make_response(render_template('add.html',**context))

    return resp

#Function manager to search the drinking places from the owners info
@app.route('/search',methods = ["GET",'POST'])
def search():
    #Render response
    #reading static file of questions to inject into questions
    questions = None
    with open(SEARCH_QUESTION,"r",encoding='utf-8') as f:
        data = json.loads(f.read())
        questions = data.get("search")

    #single from
    search_form = SearchForm()

    #answers to manage responses
    answers = session.get("answers")#get from cookies the json
    if(answers is None):
                answers = [None]*len(questions)
    
    list2 = []
    for answer in answers:
        if answer:
            answer = answer.get("value")
            list2.append(answer)
        else:
            list2.append(None)
    answers = list2

    context = {#Dictionary for the HTML page
        "key":GOOGLE_KEY,
        "add_form":search_form,
        "questions":questions,
        "answers":answers,
    }
    resp = make_response(render_template('search.html',**context))
    return resp

#Function manager to save the drinking places from the owners info
@app.route('/rate',methods = ["GET",'POST'])
def rate():
    #Render response
    #reading static file of questions to inject into questions
    questions = None
    with open(RATE_QUESTION,"r",encoding='utf-8') as f:
        data = json.loads(f.read())
        questions = data.get("create")

    #single from
    rate_form = RateForm()

    #answers to manage responses
    answers = request.cookies.get("answers")#get from cookies the json
    if(answers is not None):
        answers = answers[1:-1]#ignore the []
        answers = answers.replace(" ", "")#remove whitespace
        answers = answers.replace('"', '')#remove comillas
        answers = answers.split(",")#split by (,) Output: ['foo','foo','foo','foo','foo','foo']
    else:
        answers = [None]*len(questions)
    
    for index in range(len(answers)):
        if answers[index] == "null":
            answers[index] = None
    #Coordinates for Google
    coords =questions[1].get("options")
    if(answers[1]):
        coords = answers[1].split(";")

    context = {#Dictionary for the HTML page
        "key":GOOGLE_KEY,
        "add_form":rate_form,
        "questions":questions,
        "answers":answers,
        "coords":coords,
    }
    resp = make_response(render_template('rate.html',**context))
    resp.set_cookie('answers', json.dumps(answers))#to convert the list to a JSON object

    return resp

@app.route('/single_add/answer/<position>/<len>',methods = ['POST'])
def single_add(position,len):
    position = int(position)#transform the position input to Int
    _len = int(len)
    answers = session.get("answers")#get from cookies the json
    if not answers:
        answers = [None]*(_len)

    answers[position] = {"value":request.form["text_answer"]}#set the value in the indexed position list
    resp = make_response(redirect(url_for('add')))
    session["answers"] =  answers
    return resp

@app.route('/single_search/answer//<position>/<len>',methods = ['POST'])
def single_search(position,len):
    _len = int(len)
    position = int(position)#transform the position input to Int
    answers = session.get("answers")#get from cookies the json
    if not answers:
        answers = [None]*(_len)

    answers[position] = {"value":request.form["text_answer"]}#set the value in the indexed position list
    resp = make_response(redirect(url_for('search')))
    session["answers"] =  answers
    #TODO: send to actual db
    return resp

@app.route('/add_place/',methods = ['POST'])
def add_place():
    answers = session["answers"]#get from cookies the json
    
    coords = answers[1].get("value")#save the coords separatedly

    place = {
        "name" : answers[0].get("value"),
        "coords": coords,
        "money": answers[2].get("value"),
        "age":answers[3].get("value"),
        "mood": answers[4].get("value"),
        "music":answers[5].get("value"),
        "drink":answers[6].get("value"),
        "food":answers[7].get("value"),
        "dress":answers[8].get("value"),
    }

    create_place(place)
    resp = make_response(redirect(url_for('done')))
    session["answers"] = [None]*len(answers)
    return resp

@app.route('/search_place/',methods = ['POST'])
def search_place():
    answers = session["answers"]#get from cookies the json
    
    place_from_answer = {
        "contact" : answers[0].get("value"),
        "money": answers[1].get("value"),
        "age":answers[2].get("value"),
        "mood": answers[3].get("value"),
        "music":answers[4].get("value"),
        "drink":answers[5].get("value"),
        "food":answers[6].get("value"),
        "dress":answers[7].get("value"),
        "date": datetime.now(),
    }

    create_search(place_from_answer)
    session["place_from_answer"] = place_from_answer
    resp = make_response(redirect(url_for('result')))
    return resp

@app.route('/done')
def done():
    return render_template('done.html')

@app.route('/result')
def result():
    place_from_answer = session["place_from_answer"]
    answer = session["answers"]#get from cookies the json
    places = sort_places(place_from_answer)
    keys = []
    for place in places:
        print(place)
        for key in place:
            keys.append(key)
        print(keys,"AAAAAAAAA")

    context = {
        "answer":answer,
        "places":places,
        "keys":keys,
    }
    resp = make_response(render_template('result.html',**context))
    #session["answers"] = [None]*len(answer)

    return resp

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

