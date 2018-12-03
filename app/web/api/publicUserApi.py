import json
from flask import jsonify
from flask import request
from flask import Blueprint

from app import core
from app.services import userService
from app.web.utils import apiUtils
from app.web.schemas.userSchema import \
                                            PublicUserProfileSchema
from app.web import oauth2

api = Blueprint('public_user_api', __name__)


@api.route('/api/v1.0/public/user/profile/<user_uuid>', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_details(user_uuid):
    core.logger.debug('request=' + str(request))

    user = userService.get_user_by_uuid(user_uuid)
    data = PublicUserProfileSchema().dump(user)
    resp = apiUtils.generate_response_wrapper(data)
    return jsonify(resp)


@api.route('/api/v1.0/public/user/list', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_list():
    users = userService.get_public_users()
    user_list = []
    for u in users:
        user_list.append(PublicUserProfileSchema().dump(u))

    resp = apiUtils.generate_response_wrapper(user_list)
    return jsonify(resp)


@api.route('/api/v1.0/public/user/profiles', methods=['POST'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_details_by_list():
    core.logger.debug('request=' + str(request))
    core.logger.debug('request.data=' + str(request.data))
    user_uuid_list = json.loads(request.data)

    users = userService.get_users_by_uuid_list(user_uuid_list)
    data = []
    for u in users:
        data.append(PublicUserProfileSchema().dump(u))

    resp = apiUtils.generate_response_wrapper(data)
    return jsonify(resp)
