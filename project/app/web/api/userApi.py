
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import Blueprint

from project.app.services import userService
from project.app.web.utils import dtoUtils
from project.app.web import oauth2

api = Blueprint('user_api', __name__)


@api.route('/api/v1.0/public/user/<user_uuid>', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_by_id(user_uuid):
    # TODO get token to validate the user
    current_user = userService.get_user_by_uuid(user_uuid)
    if current_user:
        return jsonify(dtoUtils.user_serialize(current_user))
    else:
        #
        # In case we did not find the candidate by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)


@api.route('/api/v1.0/admin/user', methods=['GET'])
@oauth2.require_oauth('STAFF_ACCESS')
def get_users():
    users = userService.get_users()
    user_list = []
    for u in users:
        user_list.append(dtoUtils.user_serialize(u))

    return jsonify(user_list)


@api.route('/api/v1.0/admin/user/<user_id>', methods=['GET'])
@oauth2.require_oauth('STAFF_ACCESS')
def get_user_by_id(user_id):
    current_user = userService.get_user_by_id(user_id)
    if current_user:
        return jsonify(dtoUtils.user_serialize(current_user))
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
    user_to_be_updated = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "username": request.form["username"]
    }
    updated_user = userService.update_user(user_id, user_to_be_updated)
    if not updated_user:
        return make_response('', 404)
    else:
        return jsonify(dtoUtils.user_serialize(updated_user))


@api.route('/api/v1.0/admin/user', methods=['POST'])
@oauth2.require_oauth('STAFF_ACCESS')
def add_public_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    username = request.form["username"]
    password = request.form["password"]

    new_user = userService.add_public_user(None, username, password, first_name, last_name)

    return jsonify({
        "id": new_user.id,
        "url": url_for("user_api.getUserById", id=new_user.id)
    }), 201
