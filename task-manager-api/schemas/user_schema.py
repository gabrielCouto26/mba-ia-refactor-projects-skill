from marshmallow import Schema, fields, validate
from constants import UserRole, MIN_PASSWORD_LENGTH

class UserCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=MIN_PASSWORD_LENGTH))
    role = fields.String(dump_default=UserRole.USER.value, validate=validate.OneOf([r.value for r in UserRole]))

class UserUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=100))
    email = fields.Email()
    password = fields.String(validate=validate.Length(min=MIN_PASSWORD_LENGTH))
    role = fields.String(validate=validate.OneOf([r.value for r in UserRole]))
    active = fields.Boolean()

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
