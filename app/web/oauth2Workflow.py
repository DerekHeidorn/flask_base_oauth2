import json
from flask import Blueprint, request, session
from flask import render_template, redirect

from app.services.exceptions.security import AppAccessDeniedException
from app.services import userService, oauth2Service
from app.web.forms.user import UsernamePasswordForm, \
                                SignupForm, \
                                AccountReactivateForm, \
                                UsernamePasswordResetForm, \
                                UsernamePasswordNewForm
from app.web.forms.common import GlobalMessages
from app.web.utils import debugUtils
from app.web.resources import messages
from app.web import oauth2
from app import core

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
        form = UsernamePasswordForm()
        global_messages = GlobalMessages()
        return render_template('login.html', form=form, global_messages=global_messages)


@api.route('/login', methods=['POST'])
def login_post():

    # POST /token HTTP/1.1
    # Host: server.example.com
    # Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    # Content-Type: application/x-www-form-urlencoded
    # grant_type=password&username=johndoe&password=A3ddj3w
    form = UsernamePasswordForm()
    global_messages = GlobalMessages()

    if form.validate_on_submit():
        debugUtils.debug_request(request)
        try:
            oauth2_client = oauth2Service.query_client(form.client_id.data)
            if oauth2_client is not None:

                token_response = oauth2.create_token_response()
                debugUtils.debug_response(token_response)

                json_string = token_response.data.decode("utf-8")

                json_doc = json.JSONDecoder().decode(json_string)
                parameters = ""
                for k in json_doc:
                    if k == "error":
                        core.logger.debug("jsonDoc:" + str(json_doc))
                        error_msg = json_doc[k]
                        if 'error_description' in json_doc:
                            error_msg = json_doc['error_description']
                        # form.username.errors.append(error_msg)
                        # raise Exception(error_msg)
                        global_messages.add_global_error_msg(error_msg)
                        return render_template('login.html', form=form, global_messages=global_messages)

                    parameters += "&" + k + '=' + str(json_doc.get(k))

                redirect_url = oauth2_client.redirect_uri
                return redirect(redirect_url + "?auth_response=1" + parameters, code=302)
            else:
                core.logger.error("Client ID not found for: " + str(form.client_id.data))
                global_messages.add_global_error_msg("Client ID not found!")
                return render_template('login.html', form=form, global_messages=global_messages)
        except Exception as e:
            core.logger.debug("Exception: " + str(type(e)) + ", " + str(e))
            global_messages.add_global_error_msg(messages.errors["error.system"])
            return render_template('login.html', form=form, global_messages=global_messages)

    global_messages.add_global_error_msg(messages.errors["error.form"])
    return render_template('login.html', form=form, global_messages=global_messages)


@api.route('/signup', methods=['GET'])
def signup():

    user = current_user_in_session()
    if user:
        return redirect('/')
    else:
        form = SignupForm()
        return render_template('signup.html', form=form)


@api.route('/signup', methods=['POST'])
def signup_post():

    user = current_user_in_session()
    if user:
        return redirect('/')
    else:
        form = SignupForm()
        global_messages = GlobalMessages()

        core.logger.debug("signup_post.validate_on_submit(): " + str(form.validate_on_submit()))

        if form.validate_on_submit(): 
            try:
                oauth2_client = oauth2Service.query_client(form.client_id.data)
                if oauth2_client is not None:
                    user = userService.add_public_user(form.client_id.data,
                                                       form.alias.data,
                                                       form.username.data,
                                                       form.password.data)

                    token_response = oauth2.create_token_response()
                    json_string = token_response.data.decode("utf-8")
                    json_doc = json.JSONDecoder().decode(json_string)
                    parameters = ""
                    for k in json_doc:
                        if k == "error":
                            error_msg = json_doc[k]
                            if 'error_description' in json_doc:
                                error_msg = json_doc['error_description']
                            global_messages.add_global_error_msg(error_msg)
                            return render_template('login.html', form=form, global_messages=global_messages)

                        parameters += "&" + k + '=' + str(json_doc.get(k))

                    session['id'] = user.get_user_id()
                    redirect_url = oauth2_client.redirect_uri
                    return redirect(redirect_url + "?redirect=SuccessLogin" + parameters, code=302)
            except Exception as e:
                core.logger.debug("Exception: " + str(type(e)) + ", " + str(e))
                global_messages.add_global_error_msg(messages.errors["error.system"])
                return render_template('signup.html', form=form, global_messages=global_messages)

        global_messages.add_global_error_msg(messages.errors["error.form"])
        return render_template('signup.html', form=form, global_messages=global_messages)


@api.route('/logout')
def logout():
    if session is not None:
        session['id'] = None
    return redirect('/')


@api.route('/reactivate', methods=['GET'])
def reactivate():
    encrypted_reactivation_info = request.args.get('e')

    form = AccountReactivateForm()
    user_reactivation_code = userService.process_reactivate_account(encrypted_reactivation_info)

    form.reactivation_code = user_reactivation_code
    global_messages = GlobalMessages()
    return render_template('reactivate.html', form=form, global_messages=global_messages)


@api.route('/reactivate', methods=['POST'])
def reactivate_post():

    form = AccountReactivateForm()

    username = form.username.data
    user_reactivation_code = form.reactivation_code.data
    userService.complete_reactivate_account(username, user_reactivation_code)

    return redirect('/login')


@api.route('/reset/request', methods=['GET'])
def reset_request():

    form = UsernamePasswordResetForm()
    global_messages = GlobalMessages()
    return render_template('reset.html', form=form, global_messages=global_messages)


@api.route('/reset/request', methods=['POST'])
def reset_request_post():

    form = UsernamePasswordResetForm()
    global_messages = GlobalMessages()

    if form.validate_on_submit():
        username = form.username.data
        try:
            userService.reset_user_password(username)
        except AppAccessDeniedException as de:
            global_messages = GlobalMessages()
            global_messages.add_global_error_msg(str(de))
            return render_template('reset.html', form=form, global_messages=global_messages)

        global_messages = GlobalMessages()
        global_messages.add_global_info_msg("Reset password information to your email address")
        return render_template('reset.html', form=form, global_messages=global_messages)
    else:
        global_messages.add_global_error_msg(messages.errors["error.form"])
        return render_template('reset.html', form=form, global_messages=global_messages)


@api.route('/reset', methods=['GET'])
def reset():
    encrypted_reset_code = request.args.get('e')

    form = UsernamePasswordNewForm()
    global_messages = GlobalMessages()

    try:
        user_reset_info = userService.process_reset_user_password(encrypted_reset_code)
        form.username.data = user_reset_info['username']
        form.reset_code.data = user_reset_info['reset_code']
    except Exception as e:
        core.logger.debug("Exception: " + str(type(e)) + ", " + str(e))
        global_messages.add_global_error_msg(messages.errors["error.system"])
    return render_template('new_password.html', form=form, global_messages=global_messages)


@api.route('/reset', methods=['POST'])
def reset_post():

    form = UsernamePasswordNewForm()
    global_messages = GlobalMessages()

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            user_reset_code = form.reset_code.data
            userService.complete_reset_user_password(username, password, user_reset_code)
        except Exception as e:
            core.logger.debug("Exception: " + str(type(e)) + ", " + str(e))
            global_messages.add_global_error_msg(messages.errors["error.system"])
        return render_template('new_password.html', form=form, global_messages=global_messages)
    else:
        global_messages.add_global_error_msg(messages.errors["error.form"])
        return render_template('new_password.html', form=form, global_messages=global_messages)
