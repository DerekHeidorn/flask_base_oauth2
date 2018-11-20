# from project.app import main
from marshmallow import fields, Schema


class UsernameSchema(Schema):
    # new_username = data['new_username']
    # password = data['password']

    new_username = fields.Email(required=True)
    password = fields.String(required=True)


# 'data': data,
# 'global_info_msgs': global_info_msgs,
# 'global_warning_msgs': global_warning_msgs,
# 'global_error_msgs': global_error_msgs,
# 'field_error_msgs': field_error_msgs
# class ResponseSchema(Schema):
#     global_info_msgs = fields.List()
#     fields.