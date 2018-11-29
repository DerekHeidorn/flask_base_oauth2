import json
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import Blueprint
from marshmallow import ValidationError

from authlib.flask.oauth2 import current_token

from project.app import core
from project.app.services import userService
from project.app.web.utils import serializeUtils, apiUtils
from project.app.web.schemas.userSchema import \
    ChangePasswordSchema, ChangeUsernameSchema, \
    UserProfileBasicSchema, UserExternalBasicSchema, UserProfileDetailSchema
from project.app.web import oauth2

api = Blueprint('user_api', __name__)


@api.route('/api/v1.0/my/profile/', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_public_account():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = UserProfileBasicSchema().dump(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/account/', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_account():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = UserProfileBasicSchema().dump(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/account/profile/', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_account_profile():

    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = UserProfileDetailSchema().dump(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/user/details/<user_uuid>', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_details(user_uuid):
    core.logger.debug('request=' + str(request))

    user = userService.get_user_by_uuid(user_uuid)
    data = UserExternalBasicSchema().dump(user)
    resp = serializeUtils.generate_response_wrapper(data)
    return jsonify(resp)


@api.route('/api/v1.0/public/user/list', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_list():
    users = userService.get_public_users()
    user_list = []
    for u in users:
        user_list.append(UserExternalBasicSchema().dump(u))

    resp = serializeUtils.generate_response_wrapper(user_list)
    return jsonify(resp)


@api.route('/api/v1.0/public/user/details', methods=['POST'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_user_details_by_list():
    core.logger.debug('request=' + str(request))
    core.logger.debug('request.data=' + str(request.data))
    user_uuid_list = json.loads(request.data)

    users = userService.get_users_by_uuid_list(user_uuid_list)
    data = []
    for u in users:
        data.append(UserExternalBasicSchema().dump(u))

    resp = serializeUtils.generate_response_wrapper(data)
    return jsonify(resp)


@api.route('/api/v1.0/admin/user/all/', methods=['GET'])
@oauth2.require_oauth('ADM_ACCESS')
def get_users():
    users = userService.get_users()
    user_list = []
    for u in users:
        user_list.append(UserProfileBasicSchema().dump(u))

    resp = serializeUtils.generate_response_wrapper(user_list)
    return jsonify(resp)


@api.route('/api/v1.0/admin/account/', methods=['GET'])
@oauth2.require_oauth('ADM_ACCESS')
def get_admin_account():
    if current_token is not None and current_token.user_id is not None:

        current_user = userService.get_user_by_id(current_token.user_id)
        if current_user:
            data = UserProfileBasicSchema().dump(current_user)
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/admin/user/', methods=['POST'])
@oauth2.require_oauth('ADM_ACCESS')
def add_public_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    alias = request.form["alias"]
    username = request.form["username"]
    password = request.form["password"]

    new_user = userService.add_public_user(None, alias, username, password, first_name, last_name)

    data = UserProfileBasicSchema().dump(new_user)
    resp = serializeUtils.generate_response_wrapper(data)
    return jsonify(resp), 201


@api.route('/api/v1.0/admin/user/<user_id>', methods=['GET'])
@oauth2.require_oauth('ADM_ACCESS')
def get_user_by_id(user_id):
    current_user = userService.get_user_by_id(user_id)
    if current_user:
        data = UserProfileBasicSchema().dump(current_user)
        resp = serializeUtils.generate_response_wrapper(data)
        return jsonify(resp)
    else:
        #
        # In case we did not find the candidate by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)


@api.route('/api/v1.0/admin/user/<user_id>', methods=['DELETE'])
@oauth2.require_oauth('ADM_ACCESS')
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
@oauth2.require_oauth('ADM_ACCESS')
def update_public_user(user_id):

    user = userService.get_user_by_id(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.username = request.form["username"]

    updated_user = userService.update_user(user_id, user)
    if not updated_user:
        return make_response('', 404)
    else:
        data = UserProfileBasicSchema().dump(updated_user)
        resp = serializeUtils.generate_response_wrapper(data)
        return jsonify(resp)


@api.route('/api/v1.0/public/account/username', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_public_account_username():
    """
    get username (email)
    :return:
    """
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = {'username': current_user.username}
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/account/username', methods=['PUT'])
@oauth2.require_oauth('CUST_ACCESS')
def update_public_account_username():
    """
    Update username (email)
    :return:
    """
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user

        if current_user and current_user.user_id:
            data = json.loads(request.data)

            result = ChangeUsernameSchema().load(data)
            core.logger.debug('ChangeUsernameSchema=' + str(result))

            is_unique = userService.is_username_unique(result['new_username'], current_user.user_id)
            core.logger.debug('is_unique=' + str(is_unique))
            if not is_unique:
                raise ValidationError("Username is not unique", field_names=["new_username"])

            updated_user = userService.update_username_with_required_password(current_user.user_id,
                                                                              result['new_username'],
                                                                              result['password']
                                                                              )
            if updated_user is not None:
                data = UserProfileBasicSchema().dump(updated_user)
                resp = serializeUtils.generate_response_wrapper(data)
                return jsonify(resp)
            else:
                abort(400)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/account/username/validate', methods=['POST'])
@oauth2.require_oauth('CUST_ACCESS')
def validate_account_username():
    """
    validate username (email)
    :return:
    """
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user

        if current_user and current_user.user_id:
            data = json.loads(request.data)

            u = ChangeUsernameSchema().load(data)

            is_unique = userService.is_username_unique(u.new_username, current_user.user_id)
            if not is_unique:
                raise ValidationError("Username is not unique", field_names=["new_username"])

            data = {'is_unique': str(is_unique)}
            resp = serializeUtils.generate_response_wrapper(data)
            return jsonify(resp)

        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/public/account/password', methods=['PUT'])
@oauth2.require_oauth('CUST_ACCESS')
def update_public_account_password():
    """
    Update Password for a User Account
    :return:
    """

    if current_token is not None and current_token.user is not None:

        current_user = current_token.user

        if current_user.user_id:
            data = json.loads(request.data)
            try:
                result = ChangePasswordSchema().load(data)
                core.logger.debug('ChangePasswordSchema=' + str(result))

                userService.update_user_password(current_user.user_id,
                                                 result['old_password'],
                                                 result['new_password']
                                                 )
                resp = serializeUtils.generate_response_wrapper(None)
                return jsonify(resp)

                # data = {}
                # resp = serializeUtils.generate_response_wrapper(data)
                # return jsonify(resp)

            except ValidationError as err:
                core.logger.debug("err.messages=" + str(err.messages))
                core.logger.debug("err.valid_data=" + str(err.valid_data))
                resp = apiUtils.handle_schema_validation_error(err.messages)
                abort(resp)

        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)
