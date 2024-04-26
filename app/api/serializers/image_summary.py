from marshmallow import Schema, fields


class ImageSummarySchema(Schema):
    id = fields.UUID(dump_only=True)
    image_id = fields.Integer(dump_only=True)
    comment_count = fields.Integer(dump_only=True)
    comment_summary = fields.Str(dump_only=True)
    average_comment_length = fields.Integer(dump_only=True)
    users_commented_count = fields.Integer(dump_only=True)
    sentiment_score = fields.Integer(dump_only=True)
