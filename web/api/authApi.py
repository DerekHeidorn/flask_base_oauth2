from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from models.user import User
from services import userService
from services.utils import userUtils
from web.utils import authUtil

api = Blueprint('auth_api', __name__)



@api.route('/api/v1.0/auth/register', methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    username=post_data.get('username')

    user = userService.getUserByLogin(username)
    if not user:
        try:
            password=post_data.get('password')

            # insert the user
            newUser = userService.addUser(username, password)
            # generate the auth token
            authorities = userUtils.getUserAuthorities(newUser)
            auth_token = authUtil.encodeAuthToken(user, authorities)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201
        except Exception:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
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
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()
        if user and userUtils.isUserValid(
            user.email, post_data.get('password')
        ):
            auth_token = user.encode_auth_token(user.id)
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
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
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
        resp = User.decode_auth_token(auth_token)
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
