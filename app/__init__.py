from flask import Flask 
from flask_bootstrap import Bootstrap #Imports the bootstrap module installed in the console <<pip install -r requierments.txt>>
from .config import Config
from flask_login import LoginManager
from .auth import auth
from .models import UserModel
login_manager = LoginManager()
login_manager.login_view = "auth.login"
def create_app():
    app = Flask(__name__)                            #Inits the app from Flask class
    bootstrap = Bootstrap(app)                       #Inits the bootstrap tools from Bootstrap class. app is the instance of Flask main
    login_manager.init_app(app)
    app.config.from_object(Config)       #Configs a session key
    app.register_blueprint(auth)
    return app

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)
