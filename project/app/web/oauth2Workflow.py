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
from project.app.web.forms import forms
from project.app.web.utils import debugUtils
from project.app.web.oauth2 import authorizationServer, require_oauth, scopes

api = Blueprint('home_api', __name__)

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


@api.route('/', methods=['GET'])
def home():
    user = currentUser()
    return render_template('home.html', user=user)

@api.route('/login', methods=['GET'])
def login():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        form = forms.UsernamePasswordForm()
        return render_template('login.html', form=form)
  
# POST /token HTTP/1.1
# Host: server.example.com
# Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
# Content-Type: application/x-www-form-urlencoded
# grant_type=password&username=johndoe&password=A3ddj3w
@api.route('/login', methods=['POST'])
def loginPost():

    form = forms.UsernamePasswordForm()
    if form.validate_on_submit():
        debugUtils.debugRequest(request)
        tokenResponse = authorizationServer.create_token_response()
        debugUtils.debugResponse(tokenResponse)

        jsonString = tokenResponse.data.decode("utf-8")

        jsonDoc = json.JSONDecoder().decode(jsonString)
        parameters = ""
        for k in jsonDoc:
            parameters += "&" + k + '=' + str(jsonDoc.get(k))

        return redirect("/?redirect=SuccessLogin" + parameters, code=302)
    return render_template('login.html', form=form)

@api.route('/signup', methods=['GET'])
def signup():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        form = forms.SignupForm()
        return render_template('signup.html', form=form)


@api.route('/signup', methods=['POST'])
def signupPost():

    user = currentUser()
    if user:
        return redirect('/')
    else:
        form = forms.SignupForm()

        username = request.form['username']
        password = request.form['password']
        passwordRepeat = request.form['passwordRepeat']

        if(password == passwordRepeat): 
            user = userService.addUser(username, password)
            session['id'] = user.get_user_id()

            tokenResponse = authorizationServer.create_token_response()
            jsonString = tokenResponse.data.decode("utf-8")

            jsonDoc = json.JSONDecoder().decode(jsonString)
            parameters = ""
            for k in jsonDoc:
                parameters += "&" + k + '=' + str(jsonDoc.get(k))

            return redirect("/?redirect=SuccessLogin" + parameters, code=302)
        return redirect('/signup?error=Password')




@api.route('/logout')
def logout():
    del session['id']
    return redirect('/')








