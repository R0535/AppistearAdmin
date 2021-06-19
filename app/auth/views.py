from flask.templating import render_template
from . import  auth
from flask import  render_template,flash,session,url_for,request
from werkzeug.utils import redirect
from app.forms import LoginForm

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
        flash(f'{username}, has joined')
        session['username'] = username
        return redirect(url_for('home'))


    return render_template('login.html', **login_context)