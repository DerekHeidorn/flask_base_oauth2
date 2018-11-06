import json
from flask import Blueprint, request, session
from flask import render_template, redirect
from project.app.services import userService
from project.app.web.forms import forms
from project.app.web.utils import debugUtils
from project.app.web.oauth2 import authorizationServer

api = Blueprint('home_api', __name__)

# curl -v -u user:password localhost:9000

#  User Id is stored in the Flask Session
def currentUser():
    if 'id' in session:
        userId = session['id']
        # print("id=" + str(userId))
        user = userService.getUserById(userId)
        # print("user=" + str(user))
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
        try:
            tokenResponse = authorizationServer.create_token_response()
            debugUtils.debugResponse(tokenResponse)

            jsonString = tokenResponse.data.decode("utf-8")

            jsonDoc = json.JSONDecoder().decode(jsonString)
            parameters = ""
            for k in jsonDoc:
                if k == "error":
                    form.username.errors.append(jsonDoc['error_description'])
                    raise Exception(jsonDoc['error_description'])

                parameters += "&" + k + '=' + str(jsonDoc.get(k))

            return redirect("/?redirect=SuccessLogin" + parameters, code=302)
        except Exception as e:
            print("Exception: " + str(e), str(e.with_traceback))
            return render_template('login.html', form=form)

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

        if form.validate_on_submit(): 
            try:
                user = userService.addPublicUser(form.username.data, form.password.data)
                session['id'] = user.get_user_id()

                tokenResponse = authorizationServer.create_token_response()
                jsonString = tokenResponse.data.decode("utf-8")

                jsonDoc = json.JSONDecoder().decode(jsonString)
                parameters = ""
                for k in jsonDoc:
                    if k == "error":
                        form.username.errors.append(jsonDoc['error_description'])
                        raise Exception(jsonDoc['error_description'])                

                    parameters += "&" + k + '=' + str(jsonDoc.get(k))
            except Exception as e:
                print("Exception: " + str(e), str(e.with_traceback))
                return render_template('signup.html', form=form)

            return redirect("/?redirect=SuccessLogin" + parameters, code=302)
        return render_template('signup.html', form=form)


@api.route('/logout')
def logout():
    del session['id']
    return redirect('/')








