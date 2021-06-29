from app.models import UserData, UserModel
from flask.templating import render_template
from . import  auth
from app.firestore_service import get_user, create_user
from flask import  render_template,flash,session,url_for,request
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash

from app.forms import LoginForm
from flask_login import login_user,login_required, logout_user
@auth.route('login',methods=['GET','POST'])
def login():
    user_ip = request.remote_addr
    login_form = LoginForm()
    login_context={
        'login_form': login_form,
        'user_ip':user_ip
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            pass_from_db = user_doc.to_dict()["password"]
            print(user_doc.id,pass_from_db)
            if pass_from_db == password:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash(f'{username}, has joined')
                name = user_doc.to_dict()['username']
                session['username'] = name
                return redirect(url_for('home'))
            else:
                flash("Invalid Password")
        else:
            flash("User not found")
    return render_template('login.html', **login_context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash("See you later")
    return redirect(url_for('auth.login'))

@auth.route('signup',methods= ['GET','POST'])
def signup():
    user_ip = request.remote_addr
    signup_form =  LoginForm()
    context = {
        'signup_form': signup_form,
        'user_ip':user_ip
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)
        if user_doc.to_dict() is None:
            pwd_hash = generate_password_hash(password)
            user_data = UserData(username, pwd_hash)
            id = create_user(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')
            session['user_id'] = id
            return redirect(url_for('home'))
        else:
            flash('El usuario ya existe')
        
    return render_template('signup.html',**context)
