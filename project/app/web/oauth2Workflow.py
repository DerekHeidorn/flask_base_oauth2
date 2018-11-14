import json
from flask import Blueprint, request, session
from flask import render_template, redirect
from project.app.services import userService, oauth2Service
from project.app.web.forms import forms
from project.app.web.utils import debugUtils
from project.app.web.oauth2 import authorizationServer

api = Blueprint('home_api', __name__)


def current_user_in_session():
    #  User Id is stored in the Flask Session
    if 'id' in session:
        user_id = session['id']
        user = userService.get_user_by_id(user_id)
        return user
    return None


@api.route('/', methods=['GET'])
def home():
    user = current_user_in_session()
    return render_template('home.html', user=user)


@api.route('/login', methods=['GET'])
def login():

    user = current_user_in_session()
    if user:
        return redirect('/')
    else:
        form = forms.UsernamePasswordForm()
        return render_template('login.html', form=form)


@api.route('/reactivate', methods=['GET'])
def reactivate():
    reactivate_code = request.args.get('code')


    form = forms.UsernamePasswordReactivateForm()
    return render_template('reactivate.html', form=form)


@api.route('/reset', methods=['GET'])
def reset():
    reset_code = request.args.get('code')

    form = forms.UsernamePasswordResetForm()
    return render_template('reset.html', form=form)


@api.route('/login', methods=['POST'])
def login_post():

    # POST /token HTTP/1.1
    # Host: server.example.com
    # Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    # Content-Type: application/x-www-form-urlencoded
    # grant_type=password&username=johndoe&password=A3ddj3w
    form = forms.UsernamePasswordForm()
    if form.validate_on_submit():
        debugUtils.debug_request(request)
        try:
            oauth2_client = oauth2Service.query_client(form.client_id.data)
            if oauth2_client is not None:

                token_response = authorizationServer.create_token_response()
                debugUtils.debug_response(token_response)

                json_string = token_response.data.decode("utf-8")

                json_doc = json.JSONDecoder().decode(json_string)
                parameters = ""
                for k in json_doc:
                    if k == "error":
                        print("jsonDoc:" + str(json_doc))
                        error_msg = json_doc[k]
                        if 'error_description' in json_doc:
                            error_msg = json_doc['error_description']
                        form.username.errors.append(error_msg)
                        raise Exception(error_msg)

                    parameters += "&" + k + '=' + str(json_doc.get(k))

                redirect_url = oauth2_client.redirect_uri
                return redirect(redirect_url + "?auth_response=1" + parameters, code=302)
        except Exception as e:
            print("Exception: " + str(e))
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@api.route('/signup', methods=['GET'])
def signup():

    user = current_user_in_session()
    if user:
        return redirect('/')
    else:
        form = forms.SignupForm()
        return render_template('signup.html', form=form)


@api.route('/signup', methods=['POST'])
def signup_post():

    user = current_user_in_session()
    if user:
        return redirect('/')
    else:
        form = forms.SignupForm()

        if form.validate_on_submit(): 
            try:
                oauth2_client = oauth2Service.query_client(form.client_id.data)
                if oauth2_client is not None:
                    user = userService.add_public_user(form.client_id.data, form.username.data, form.password.data)

                    token_response = authorizationServer.create_token_response()
                    json_string = token_response.data.decode("utf-8")
                    json_doc = json.JSONDecoder().decode(json_string)
                    parameters = ""
                    for k in json_doc:
                        if k == "error":
                            error_msg = json_doc[k]
                            if 'error_description' in json_doc:
                                error_msg = json_doc['error_description']
                            form.username.errors.append(error_msg)
                            raise Exception(error_msg)

                        parameters += "&" + k + '=' + str(json_doc.get(k))

                    session['id'] = user.get_user_id()
                    redirect_url = oauth2_client.redirect_uri
                    return redirect(redirect_url + "?redirect=SuccessLogin" + parameters, code=302)
            except Exception as e:
                form.username.errors.append(e)
                return render_template('signup.html', form=form)

        return render_template('signup.html', form=form)


@api.route('/logout')
def logout():
    if session is not None:
        session['id'] = None
    return redirect('/')
