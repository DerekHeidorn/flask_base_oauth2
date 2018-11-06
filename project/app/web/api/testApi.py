from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from authlib.flask.oauth2 import current_token

from project.app.models.user import User
from project.app.services import userService
from project.app.services.utils import userUtils
from project.app.web.utils import authUtils
from project.app.web.oauth2 import require_oauth

api = Blueprint('test_api', __name__)

@api.route('/api/v1.0/test/valid', methods=['GET'])
@require_oauth('CUST_ACCESS')
def validAuthority():
    print("current_token=" + str(current_token))
    #user = current_token.user
    user = userService.getUserById(current_token.user_id)
    return jsonify(valid=True, username=user.username)

@api.route('/api/v1.0/test/invalid', methods=['GET'])
@require_oauth('NO_ACCESS_TEST')
def invalidAuthority():
    print("current_token=" + str(current_token))
    #user = current_token.user
    user = userService.getUserById(current_token.user_id)
    return jsonify(invalid=True, username=user.username)


