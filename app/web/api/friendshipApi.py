from flask import Blueprint
from flask import jsonify
from flask import abort

from authlib.flask.oauth2 import current_token
from app.services.utils import sha256
from app.services import friendshipService
from app.web import oauth2
from app.web.utils import apiUtils
from app.web.schemas.userSchema import PublicUserProfileSchema

api = Blueprint('friendship_api', __name__)


@api.route('/api/v1.0/my/friends', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_friends():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            friends = friendshipService.get_friends_by_user_id(current_user.user_id)

            pending_list = []
            accepted_list = []
            for u in friends["pending_friends"]:
                pending_list.append(PublicUserProfileSchema().dump(u))

            for u in friends["accepted_friends"]:
                accepted_list.append(PublicUserProfileSchema().dump(u))

            data = {"pending_friends": pending_list, "accepted_friends": accepted_list}

            resp = apiUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:

            abort(403)
    else:
        abort(401)


@api.route('/api/v1.0/my/friend/user/<user_uuid>/<user_digest>', methods=['post'])
@oauth2.require_oauth('GRP_ACCESS')
def friend_user(user_uuid, user_digest):

    if current_token is not None and current_token.user is not None:
        my_user_uuid = current_token.user.user_uuid

        digest_to_compare = sha256.hexdigest(user_uuid)

        if digest_to_compare == user_digest:
            friends = friendshipService.add_pending_friendship(my_user_uuid, user_uuid)

            friend_list = []
            if friends is not None:
                for u in friends:
                    friend_list.append(PublicUserProfileSchema().dump(u))

            resp = apiUtils.generate_response_wrapper(friend_list)
            resp = apiUtils.add_global_success_msg(resp, "Requesting friendship sent")

            return jsonify(resp), 201
        else:
            abort(403)
    else:
        abort(403)


@api.route('/api/v1.0/my/unfriend/user/<user_uuid>/<user_digest>', methods=['put'])
@oauth2.require_oauth('GRP_ACCESS')
def unfriend_user(user_uuid, user_digest):

    if current_token is not None and current_token.user is not None:
        my_user_uuid = current_token.user.user_uuid

        digest_to_compare = sha256.hexdigest(user_uuid)

        if digest_to_compare == user_digest:
            friends = friendshipService.remove_accepted_friendship(my_user_uuid, user_uuid)

            friend_list = []
            if friends is not None:
                for u in friends:
                    friend_list.append(PublicUserProfileSchema().dump(u))

            resp = apiUtils.generate_response_wrapper(friend_list)
            resp = apiUtils.add_global_success_msg(resp, "Removed friend")
            return jsonify(resp), 200
        else:
            abort(403)
    else:
        abort(403)
