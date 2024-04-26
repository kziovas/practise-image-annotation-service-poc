from flask import Blueprint, jsonify, request
from app.models import Comment
from app.models import Image
from app.models import User
from app.core_services import db
from app.api.serializers.comment import CommentSchema

comment_blueprint = Blueprint('comment', __name__)
comment_schema = CommentSchema()

@comment_blueprint.route('/comment', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify(comment_schema.dump(comments, many=True)), 200

@comment_blueprint.route('/comment/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        return jsonify(comment_schema.dump(comment)), 200
    else:
        return jsonify({'message': 'Comment not found'}), 404

@comment_blueprint.route('/comment', methods=['POST'])
def create_comment():
    data = request.json
    if not data:
        return jsonify({'message': 'No comment data provided'}), 400
    
    user_id=data.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    image_id=data.get("image_id")
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'message': 'Image not found'}), 404
    
    new_comment = Comment(body=data.get('body'), user_id=user_id,image_id=image_id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(comment_schema.dump(new_comment)), 201

@comment_blueprint.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404
    db.session.delete(comment)
    db.session.commit()
    return '', 204
