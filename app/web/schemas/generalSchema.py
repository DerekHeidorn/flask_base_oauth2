
from marshmallow import fields, Schema


class CodeTableSchema(Schema):
    code = fields.Function(lambda obj: obj.code.strip())
    description = fields.Function(lambda obj: obj.description.strip())
