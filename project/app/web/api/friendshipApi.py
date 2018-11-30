from flask import Blueprint
from flask import jsonify
from flask import abort

from authlib.flask.oauth2 import current_token
from project.app.services import friendshipService
from project.app.web import oauth2
from project.app.web.utils import serializeUtils
from project.app.web.schemas.userSchema import PublicUserProfileSchema

api = Blueprint('friendship_api', __name__)


@api.route('/api/v1.0/my/friends', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_friends():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            friends = friendshipService.get_friends_by_user_id(current_user.user_id)

            user_list = []
            for u in friends:
                user_list.append(PublicUserProfileSchema().dump(u))

            resp = serializeUtils.generate_response_wrapper(user_list)
            return jsonify(resp)
        else:

            abort(403)
    else:
        abort(401)
