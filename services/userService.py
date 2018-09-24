import hashlib
import json

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import Blueprint




from math import ceil

from models.user import User
from persist import userDao
from services.baseService import BaseService
from services.utils.userUtils import randomUserPrivateKey
from services.utils.userUtils import get_hashed_password
from services.utils.userUtils import is_user_valid as util_is_user_valid


# class UserService(BaseService):

api = Blueprint('userService_api', __name__)

def get_error_code(error):
    if "parameter" in error.message.lower():
        return 9100

    return 9000

def is_user_valid(username, password):
    user = userDao.get_user_by_login(username)
    if(user is not None):
        return util_is_user_valid(user, password)
    else:
        return False


def build_message(key, message):
    return {key:message}    

@api.route('/api/v1.0/user/<id>', methods=['GET'])
#@oauth.require_oauth('email')
def user_by_id(id):
    current_user = userDao.get_user(id, serialize=True)
    if current_user:
        return jsonify({"user": current_user})
    else:
        #
        # In case we did not find the candidate by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)




@api.route('/api/v1.0/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        if userDao.delete_user(id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["X-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["X-APP-ERROR-MESSAGE"] = err
        return tmp_response



@api.route('/api/v1.0/user/<id>', methods=['PUT'])
def update_user(id):
    user_to_be_updated = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "login":request.form["login"]
    }
    updated_user = userDao.update_user(id, user_to_be_updated)
    if not updated_user:
        return make_response('', 404)
    else:
        return jsonify({"user": updated_user})


@api.route('/api/v1.0/user', methods=['POST'])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    login = request.form["login"]
    password = request.form["password"]

    randomUserPrivateKey(32)

    newUser = User(first_name=first_name, last_name=last_name, login=login)
    newUser.status_cd = 'A'
    newUser.type_cd = '1'
    newUser.failed_attempt_cnt = 0
    newUser.private_key = randomUserPrivateKey(32)
    newUser.password_salt = randomUserPrivateKey(32) 
    newUser.password_hash = get_hashed_password(password, newUser.password_salt)
    

    new_user_id = userDao.add_user(newUser)

    return jsonify({
        "id": new_user_id,
        "url": url_for("userService_api.user_by_id", id=new_user_id)
    })



