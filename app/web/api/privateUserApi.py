import json
from flask import jsonify
from flask import abort
from flask import request
from flask import Blueprint
from marshmallow import ValidationError

from authlib.flask.oauth2 import current_token

from app import core
from app.services import userService
from app.web.utils import apiUtils
from app.web.schemas.userSchema import \
    ChangePasswordSchema, ChangeUsernameSchema, \
    PrivateUserAccountSchema, PrivateUserPreferencesSchema, PublicUserProfileSchema, \
    ChangeUserNamesSchema, ChangePrivateSchema
from app.web import oauth2

api = Blueprint('private_user_api', __name__)


@api.route('/api/v1.0/my/profile', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_public_public():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = PublicUserProfileSchema().dump(current_user)
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


@api.route('/api/v1.0/my/preferences', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_preferences():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = PrivateUserPreferencesSchema().dump(current_user)
            resp = apiUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/my/preferences/names', methods=['PUT'])
@oauth2.require_oauth('CUST_ACCESS')
def update_my_preferences_names():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = json.loads(request.data)
            core.logger.debug('data=' + str(data))

            names_to_update = ChangeUserNamesSchema().load(data)
            core.logger.debug('ChangeUserNamesSchema=' + str(names_to_update))

            user = userService.update_user_names(current_user.user_uuid,
                                                 names_to_update['first_name'],
                                                 names_to_update['last_name'])
            if user:
                data = PrivateUserPreferencesSchema().dump(user)
                resp = apiUtils.generate_response_wrapper(data)
                resp = apiUtils.add_global_success_msg(resp, "Successfully update your names")
                return jsonify(resp)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(401)


@api.route('/api/v1.0/my/preferences/private', methods=['PUT'])
@oauth2.require_oauth('CUST_ACCESS')
def update_my_preferences_private():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = json.loads(request.data)
            core.logger.debug('data=' + str(data))

            private_fl_to_update = ChangePrivateSchema().load(data)
            core.logger.debug('ChangePrivateSchema=' + str(private_fl_to_update))

            user = userService.update_user_private_fl(current_user.user_uuid,
                                                      private_fl_to_update['is_private'])
            if user:
                data = PrivateUserPreferencesSchema().dump(user)
                resp = apiUtils.generate_response_wrapper(data)
                return jsonify(resp)
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(401)


@api.route('/api/v1.0/my/account', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_account():
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = PrivateUserAccountSchema().dump(current_user)
            resp = apiUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/my/account/username', methods=['GET'])
@oauth2.require_oauth('CUST_ACCESS')
def get_my_account_username():
    """
    get username (email)
    :return:
    """
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user
        if current_user:
            data = {'username': current_user.username}
            resp = apiUtils.generate_response_wrapper(data)
            return jsonify(resp)
        else:
            #
            # In case we did not find the candidate by id
            # we send HTTP 404 - Not Found error to the client
            #
            abort(404)
    else:
        abort(401)


@api.route('/api/v1.0/my/account/username', methods=['PUT'])
@oauth2.require_oauth('CUST_ACCESS')
def update_my_account_username():
    """
    Update username (email)
    :return:
    """
    if current_token is not None and current_token.user is not None:

        current_user = current_token.user

        if current_user and current_user.user_id:
            data = json.loads(request.data)
            core.logger.debug('data=' + str(data))

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
                data = PrivateUserAccountSchema().dump(updated_user)
                resp = apiUtils.generate_response_wrapper(data)
                resp = apiUtils.add_global_success_msg(resp, "Successfully update your email")
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


@api.route('/api/v1.0/my/account/password', methods=['PUT'])
@oauth2.require_oauth('CUST_ACCESS')
def update_my_account_password():
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
                resp = apiUtils.generate_response_wrapper(None)
                resp = apiUtils.add_global_success_msg(resp, "Successfully update your password")
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
