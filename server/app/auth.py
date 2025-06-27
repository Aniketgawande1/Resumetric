from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)
users = {}  # Simple in-memory storage

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email in users:
        return jsonify({'msg': 'User already exists'}), 400
    users[email] = password
    return jsonify({'msg': 'Registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if users.get(email) != password:
        return jsonify({'msg': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)
