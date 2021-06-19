from flask import Flask 
from flask_bootstrap import Bootstrap #Imports the bootstrap module installed in the console <<pip install -r requierments.txt>>
from .config import Config

from .auth import auth
def create_app():
    app = Flask(__name__)                            #Inits the app from Flask class
    bootstrap = Bootstrap(app)                       #Inits the bootstrap tools from Bootstrap class. app is the instance of Flask main
    app.config.from_object(Config)       #Configs a session key
    app.register_blueprint(auth)
    return app