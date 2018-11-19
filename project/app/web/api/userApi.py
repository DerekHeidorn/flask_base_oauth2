
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import Blueprint

from authlib.flask.oauth2 import current_token

from project.app.services import userService
from project.app.web.utils import serializeUtils
from project.app.web import oauth2

api = Blueprint('user_api', __name__)


@api.route('/api/v1.0/public/account/', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_account():
    if current_token is not None and current_token.user_id is not None:

        current_user = userService.get_user_by_id(current_token.user_id)
        if current_user:
            data = serializeUtils.serialize_user(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/account/profile/', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_account_profile():

    if current_token is not None and current_token.user_id is not None:

        current_user = userService.get_user_by_id(current_token.user_id)
        if current_user:
            data = serializeUtils.serialize_user_profile(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/admin/user/all/', methods=['GET'])
@oauth2.require_oauth('STAFF_ACCESS')
def get_users():
    users = userService.get_users()
    user_list = []
    for u in users:
        user_list.append(serializeUtils.serialize_user(u))

    resp = serializeUtils.generate_response_wrapper(user_list)
    return jsonify(resp)


@api.route('/api/v1.0/admin/account/', methods=['GET'])
@oauth2.require_oauth('STAFF_ACCESS')
def get_admin_account():
    if current_token is not None and current_token.user_id is not None:

        current_user = userService.get_user_by_id(current_token.user_id)
        if current_user:
            data = serializeUtils.serialize_user(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/admin/user/', methods=['POST'])
@oauth2.require_oauth('STAFF_ACCESS')
def add_public_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    username = request.form["username"]
    password = request.form["password"]

    new_user = userService.add_public_user(None, username, password, first_name, last_name)

    data = serializeUtils.serialize_user(new_user)
    resp = serializeUtils.generate_response_wrapper(data)
    return jsonify(resp), 201


@api.route('/api/v1.0/admin/user/<user_id>', methods=['GET'])
@oauth2.require_oauth('STAFF_ACCESS')
def get_user_by_id(user_id):
    current_user = userService.get_user_by_id(user_id)
    if current_user:
        data = serializeUtils.serialize_user(current_user)
        resp = serializeUtils.generate_response_wrapper(data)
        return jsonify(resp)
    else:
        #
        # In case we did not find the candidate by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)


@api.route('/api/v1.0/admin/user/<user_id>', methods=['DELETE'])
@oauth2.require_oauth('STAFF_ACCESS')
def delete_user(user_id):
    try:
        if userService.delete_user(user_id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError:
        tmp_response = make_response("", 500)
        return tmp_response


@api.route('/api/v1.0/admin/user/<user_id>', methods=['PUT'])
@oauth2.require_oauth('STAFF_ACCESS')
def update_public_user(user_id):

    user = userService.get_user_by_id(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.username = request.form["username"]

    updated_user = userService.update_user(user_id, user)
    if not updated_user:
        return make_response('', 404)
    else:
        data = serializeUtils.serialize_user(updated_user)
        resp = serializeUtils.generate_response_wrapper(data)
        return jsonify(resp)
