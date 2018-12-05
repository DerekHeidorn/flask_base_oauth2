import json
from flask import jsonify
from flask import request
from flask import Blueprint
from flask import abort
from authlib.flask.oauth2 import current_token

from app import core
from app.services import userService, friendshipService
from app.web.utils import apiUtils
from app.web.schemas.userSchema import \
                                            PublicUserProfileSchema
from app.web import oauth2

api = Blueprint('public_user_api', __name__)


@api.route('/api/v1.0/public/user/profile/<user_uuid>', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_details(user_uuid):
    core.logger.debug('request=' + str(request))

    if current_token is not None and current_token.user is not None:
        current_user = current_token.user

        if current_user:
            user = userService.get_user_by_uuid(user_uuid)
            if user:
                d = PublicUserProfileSchema().dump(user)
                friendships = friendshipService.get_friendships_by_user_id(current_user.user_id)
                d['is_friend'] = False

                for f in friendships:
                    if f.user_id == user.user_id or f.friend_user_id == user.user_id:
                        d['is_friend'] = True
                        break

                resp = apiUtils.generate_response_wrapper(d)
                return jsonify(resp)
            else:
                abort(404)
        else:
            abort(403)
    else:
        abort(401)


@api.route('/api/v1.0/public/user/list', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_list():

    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        user_list = list()
        if current_user:
            friends = friendshipService.get_friends_by_user_id(current_user.user_id)
            users = userService.get_public_users()

            for u in users:
                d = PublicUserProfileSchema().dump(u)
                d['is_friend'] = False

                for f in friends["pending_friend_requests"]:
                    if f.user_id == u.user_id:
                        d['is_friend'] = True
                        break

                for f in friends["pending_friends"]:
                    if f.user_id == u.user_id:
                        d['is_friend'] = True
                        break

                for f in friends["accepted_friends"]:
                    if f.user_id == u.user_id:
                        d['is_friend'] = True
                        break

                user_list.append(d)

        resp = apiUtils.generate_response_wrapper(user_list)
        return jsonify(resp)
    else:
        abort(403)


@api.route('/api/v1.0/public/user/profiles', methods=['POST'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_details_by_list():
    core.logger.debug('request=' + str(request))
    core.logger.debug('request.data=' + str(request.data))
    user_uuid_list = json.loads(request.data)

    users = userService.get_users_by_uuid_list(user_uuid_list)
    core.logger.debug('users=' + str(users))
    data = []
    if users is not None:
        for u in users:
            core.logger.debug('**u=' + str(u))
            data.append(PublicUserProfileSchema().dump(u))

    resp = apiUtils.generate_response_wrapper(data)
    return jsonify(resp)
