import hashlib
import json
#from oauthlib import 

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import Blueprint
from datetime import datetime, timedelta

import jwt

from math import ceil

from project.app.models.user import User
from project.app.services import userService, commonService
from project.app.services.utils import userUtils
from project.app.web.utils import dtoUtils
from project.app.web import oauth2

#  authorities = userUtils.getUserAuthorities(user)
# class UserService(BaseService):

api = Blueprint('user_api', __name__)

def getErrorCode(error):
    if "parameter" in error.message.lower():
        return 9100

    return 9000


@api.route('/api/v1.0/admin/user/<id>', methods=['GET'])
@oauth2.require_oauth('STAFF_ACCESS')
def getUserById(id):
    current_user = userService.getUserById(id)
    if current_user:
        return jsonify(dtoUtils.userSerialize(current_user))
    else:
        #
        # In case we did not find the candidate by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)

@api.route('/api/v1.0/admin/user/<id>', methods=['DELETE'])
@oauth2.require_oauth('STAFF_ACCESS')
def deleteUser(id):
    try:
        if userService.deleteUser(id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["X-APP-ERROR-CODE"] = getErrorCode(err)
        tmp_response.headers["X-APP-ERROR-MESSAGE"] = err
        return tmp_response



@api.route('/api/v1.0/admin/user/<id>', methods=['PUT'])
@oauth2.require_oauth('STAFF_ACCESS')
def updatePublicUser(id):
    user_to_be_updated = {
        "firstName":request.form["firstName"],
        "lastName":request.form["lastName"],
        "username":request.form["username"]
    }
    updated_user = userService.updateUser(id, user_to_be_updated)
    if not updated_user:
        return make_response('', 404)
    else:
        return jsonify(dtoUtils.userSerialize(updated_user))

@api.route('/api/v1.0/admin/user', methods=['POST'])
@oauth2.require_oauth('STAFF_ACCESS')
def addPublicUser():
    firstName = request.form["firstName"]
    lastName = request.form["lastName"]
    username = request.form["username"]
    password = request.form["password"]

    newUser = userService.addUser(username, password, firstName, lastName)

    return jsonify({
        "id": newUser.id,
        "url": url_for("user_api.getUserById", id=newUser.id)
    }), 201
    


 



