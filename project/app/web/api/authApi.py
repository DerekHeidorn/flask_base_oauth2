from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from authlib.flask.oauth2 import current_token

from project.app.models.user import User
from project.app.services import userService
from project.app.services.utils import userUtils
from project.app.web.utils import authUtils
from project.app.web.oauth2 import require_oauth

api = Blueprint('auth_api', __name__)

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

@api.route('/api/v1.0/auth/register', methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    username=post_data.get('username')

    user = userService.getUserByUsername(username)
    if not user:
        try:
            password=post_data.get('password')

            # insert the user
            newUser = userService.addUser(username, password)
            print("added new user(1):" +str(newUser))
            # generate the auth token
            authorities = userUtils.getUserAuthorities(newUser)
            print("added authorities(2):" + str(authorities))
            auth_token = authUtils.encodeAuthToken(newUser, authorities)
            print("added auth_token(3):")
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            print("added make_response(4):")
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            print("Exception: " + str(e), str(e.with_traceback))
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


"""
User Login Resource
"""
@api.route('/api/v1.0/auth/login', methods=['POST'])
def login():
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = userService.getUserByUsername(post_data.get('username'))
        
        if user is not None and userUtils.isUserValid(user, post_data.get('password')):
            authorities = userUtils.getUserAuthorities(user)
            auth_token = authUtils.encodeAuthToken(user, authorities)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


"""
User Resource
"""
@api.route('/api/v1.0/auth/status', methods=['GET'])
def status():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        auth_token = ''
    if auth_token:
        resp = authUtils.decodeAuthToken(auth_token)
        if not isinstance(resp, str):
            user = userService.getUserById(id=resp)
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'username': user.username
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 401


"""
Logout Resource
"""
@api.route('/api/v1.0/auth/logout', methods=['POST'])
def logout():
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = authUtils.decodeAuthToken(auth_token)
        if not isinstance(resp, str):
            try:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403
