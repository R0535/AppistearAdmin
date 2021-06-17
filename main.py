from flask import Flask, request,render_template #request: Contains the self-elements of the request entity
from flask.helpers import make_response          #render_template: the html files manager. secondary parameters managed as cookies render_template("file.html", some_data = some_data)
from werkzeug.utils import redirect              #redirect: to create hubs where can be managed security or other stuff
from flask_bootstrap import Bootstrap            #Imports the bootstrap module installed in the console <<pip install -r requierments.txt>>
app = Flask(__name__)                            #Inits the app from Flask class
bootstrap = Bootstrap(app)                       #Inits the bootstrap tools from Bootstrap class. app is the instance of Flask main
app.config['SECRET_KEY'] = 'SUPER SECRET'        #Configs a session key

todos = ['TODO1','TODO2','TODO3','TODO4']

@app.route("/")                                  #URL decorator with URI name / = root   
def index():                                     #The def name for the routing behaivour
    user_ip = request.remote_addr                #module Request from flask (remote_addr) is the Clients IP
    response = make_response(redirect("/hello")) #Building a response manually. Redirecting to other URI behaivour
    response.set_cookie('user_ip',user_ip)       #set_cookie is part of the context of the response made
    return response                              #returned the response to the client. 

@app.route('/hello')                             #URL decorator with URI name /hello = welcome page
def hello():                                     #The def name for the routing behaivour
    user_ip = request.cookies.get('user_ip')     #session client ip called from the cookie setted in line <<response.set_cookie(user_ip . . .)>>

    context = {                                  #Dictionary for the main app-data
        "user_ip": user_ip,
        "todos": todos,
    }

    return render_template('hello.html',**context) #returned the response to the client. This time, with the html page