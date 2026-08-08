from marshmallow import Schema, fields, validate
from constants import DEFAULT_COLOR

class CategoryCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(load_default='')
    color = fields.String(load_default=DEFAULT_COLOR, validate=validate.Regexp(r'^#[0-9a-fA-F]{6}$'))

class CategoryUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String()
    color = fields.String(validate=validate.Regexp(r'^#[0-9a-fA-F]{6}$'))
