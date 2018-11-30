from marshmallow import fields, Schema
from project.app.services.utils import sha256


class UserProfileBasicSchema(Schema):
    user_uuid = fields.String(required=True)
    username = fields.Email(required=True)
    alias = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
    formatted_name = fields.Method('get_formatted_name')

    def get_formatted_name(self, obj):
        return obj.get_formatted_name()


class UserProfileDetailSchema(Schema):
    user_uuid = fields.String(required=True)
    username = fields.Email(required=True)
    alias = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
    formatted_name = fields.Method('get_formatted_name')

    def get_formatted_name(self, obj):
        return obj.get_formatted_name()


class UserExternalBasicSchema(Schema):
    user_uuid = fields.String(required=True)
    alias = fields.String(required=True)

    user_uuid_digest = fields.Method('get_digest')

    def get_digest(self, obj):
        if obj.user_uuid is not None:
            return sha256.hexdigest(str(obj.user_uuid))
        return None


class ChangeUsernameSchema(Schema):

    new_username = fields.Email(required=True)
    password = fields.String(required=True)


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)
