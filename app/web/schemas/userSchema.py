from marshmallow import fields, Schema
from app.services.utils import sha256


class PrivateUserAccountSchema(Schema):
    user_uuid = fields.String(required=True)
    username = fields.Email(required=True)
    alias = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
    formatted_name = fields.Method('get_formatted_name')

    def get_formatted_name(self, obj):
        return obj.get_formatted_name()


class PrivateUserPreferencesSchema(Schema):
    user_uuid = fields.String(required=True)
    username = fields.Email(required=True)
    alias = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
    formatted_name = fields.Method('get_formatted_name')
    is_private = fields.Boolean()
    account_type = fields.Method('get_account_type')

    def get_formatted_name(self, obj):
        return obj.get_formatted_name()

    def get_account_type(self, obj):
        return "Basic"


class PublicUserProfileSchema(Schema):
    user_uuid = fields.String(required=True)
    alias = fields.String(required=True)
    is_friend = False

    user_uuid_digest = fields.Method('get_digest')

    def get_digest(self, obj):
        if obj.user_uuid is not None:
            return sha256.hexdigest(str(obj.user_uuid))
        return None


class ChangeUserNamesSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class ChangePrivateSchema(Schema):
    is_private = fields.Boolean(required=True)


class ChangeUsernameSchema(Schema):
    old_username = fields.String(required=True)
    new_username = fields.Email(required=True)
    password = fields.String(required=True)


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)
