from flask import Blueprint, jsonify, request
from app.models import User
from app.core_services import db
from app.api.serializers.user import UserSchema

user_blueprint = Blueprint('user', __name__)
user_schema = UserSchema()


@user_blueprint.route('/user/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)), 200


@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@user_blueprint.route('/user/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@user_blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return jsonify({'message': 'No user data provided'}), 400
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_user = User(username=data.get('username'), email=data.get('email'), password_hash=data.get('password_hash'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user)), 201


@user_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.json
    if not data:
        return jsonify({'message': 'No user data provided'}), 400
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password_hash = data.get('password_hash', user.password_hash)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 200


@user_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return '', 204
