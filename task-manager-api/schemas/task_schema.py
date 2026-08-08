from marshmallow import Schema, fields, validate, post_load
from constants import TaskStatus, TaskPriority, MIN_TITLE_LENGTH, MAX_TITLE_LENGTH
from datetime import datetime

class TaskCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=MIN_TITLE_LENGTH, max=MAX_TITLE_LENGTH))
    description = fields.String(load_default='')
    status = fields.String(load_default=TaskStatus.PENDING.value, validate=validate.OneOf([s.value for s in TaskStatus]))
    priority = fields.Integer(load_default=TaskPriority.MEDIUM.value, validate=validate.OneOf([p.value for p in TaskPriority]))
    user_id = fields.Integer(allow_none=True)
    category_id = fields.Integer(allow_none=True)
    due_date = fields.Date(allow_none=True)
    tags = fields.Raw(allow_none=True)

    @post_load
    def process_tags(self, data, **kwargs):
        if 'tags' in data and isinstance(data['tags'], list):
            data['tags'] = ','.join(data['tags'])
        return data

class TaskUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=MIN_TITLE_LENGTH, max=MAX_TITLE_LENGTH))
    description = fields.String(allow_none=True)
    status = fields.String(validate=validate.OneOf([s.value for s in TaskStatus]))
    priority = fields.Integer(validate=validate.OneOf([p.value for p in TaskPriority]))
    user_id = fields.Integer(allow_none=True)
    category_id = fields.Integer(allow_none=True)
    due_date = fields.Date(allow_none=True)
    tags = fields.Raw(allow_none=True)

    @post_load
    def process_tags(self, data, **kwargs):
        if 'tags' in data and isinstance(data['tags'], list):
            data['tags'] = ','.join(data['tags'])
        return data

class TaskSearchSchema(Schema):
    q = fields.String(load_default='')
    status = fields.String(load_default='')
    priority = fields.Integer(allow_none=True)
    user_id = fields.Integer(allow_none=True)
