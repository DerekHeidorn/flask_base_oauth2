# from project.app import main
from marshmallow import fields, Schema


class ChangeUsernameSchema(Schema):

    new_username = fields.Email(required=True)
    password = fields.String(required=True)


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)

