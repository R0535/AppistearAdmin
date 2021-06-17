from flask import Flask, request,render_template #request: Contains the self-elements of the request entity
from flask.helpers import make_response          #render_template: the html files manager. secondary parameters managed as cookies render_template("file.html", some_data = some_data)
from werkzeug.utils import redirect              #redirect: to create hubs where can be managed security or other stuff

app = Flask(__name__)

todos = ['TODO1','TODO2','TODO3','TODO4']

@app.route("/")
def index():
    user_ip = request.remote_addr
    response = make_response(redirect("/hello"))
    response.set_cookie('user_ip',user_ip)
    return response

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')

    context = {
        "user_ip": user_ip,
        "todos": todos,
    }

    return render_template('hello.html',**context)