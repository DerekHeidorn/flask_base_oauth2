import json
from flask import Blueprint, request, session
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from authlib.specs.rfc6749 import OAuth2Error

from project.app.models.user import User
from project.app.models.oauth2 import OAuth2Client
from project.app.services import userService, oauth2Service
from project.app.services.utils import userUtils
from project.app.web.utils import debugUtils
from project.app.web.oauth2 import authorizationServer, require_oauth, scopes

bp = Blueprint(__name__, 'home')

# curl -v -u user:password localhost:9000

#  User Id is stored in the Flask Session
def currentUser():
    if 'id' in session:
        userId = session['id']
        print("id=" + str(userId))
        user = userService.getUserById(userId)
        print("user=" + str(user))
        return user
    return None


@bp.route('/', methods=['GET'])
def home():
    user = currentUser()
    return render_template('home.html', user=user)

@bp.route('/login', methods=['GET'])
def login():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        return render_template('login.html')
  
@bp.route('/signup', methods=['GET'])
def signup():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        return render_template('signup.html')


@bp.route('/signup', methods=['POST'])
def signupPost():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        username = request.form['username']
        password = request.form['password']
        passwordRepeat = request.form['passwordRepeat']

        if(password == passwordRepeat): 
            user = userService.addUser(username, password)
            session['id'] = user.get_user_id()
            return redirect('/')
        return redirect('/signup?error=Password')

# POST /token HTTP/1.1
# Host: server.example.com
# Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
# Content-Type: application/x-www-form-urlencoded
# grant_type=password&username=johndoe&password=A3ddj3w
@bp.route('/oauth/authorize', methods=['POST'])
def issue_token():

    debugUtils.debugRequest(request)
    tokenResponse = authorizationServer.create_token_response()
    debugUtils.debugResponse(tokenResponse)

    jsonString = tokenResponse.data.decode("utf-8")

    jsonDoc = json.JSONDecoder().decode(jsonString)
    parameters = ""
    for k in jsonDoc:
        parameters += "&" + k + '=' + str(jsonDoc.get(k))

    return redirect("/?redirect=SuccessLogin" + parameters, code=302)


@bp.route('/oauth/logout')
def logout():
    del session['id']
    return redirect('/')








