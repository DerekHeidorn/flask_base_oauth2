from marshmallow import fields, Schema


class UserProfileBasicSchema(Schema):
    user_uuid = fields.String(required=True)
    username = fields.Email(required=True)
    alias = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    formatted_name = fields.Method('get_formatted_name')

    def get_formatted_name(self, obj):
        return obj.get_formatted_name()


class UserProfileDetailSchema(Schema):
    user_uuid = fields.String(required=True)
    username = fields.Email(required=True)
    alias = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    formatted_name = fields.Method('get_formatted_name')

    def get_formatted_name(self, obj):
        return obj.get_formatted_name()


class UserExternalBasicSchema(Schema):
    user_uuid = fields.String(required=True)
    alias = fields.String(required=True)


class ChangeUsernameSchema(Schema):

    new_username = fields.Email(required=True)
    password = fields.String(required=True)


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)
