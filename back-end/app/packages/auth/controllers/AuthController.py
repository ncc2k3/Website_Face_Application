from flask import Blueprint, request, jsonify
from app.packages.auth.services.AuthService import AuthService
import uuid
import os

auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService()

# Routes: auth/login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    return auth_service.authenticate_user(email, password)

# Routes: auth/login_face
@auth_blueprint.route('/login_face', methods=['POST'])
def login_face():
    image_file = request.files.get('image')

    if image_file is None:
        return jsonify({"error": "No image provided"}), 400

    return auth_service.authenticate_by_face(image_file)

# Routes: auth/register
@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    return auth_service.register_user(first_name, last_name, email, password)

# Routes: auth/register_face
@auth_blueprint.route('/register_face', methods=['POST'])
def register_face():
    email = request.form.get('email')
    image_file = request.files.get('image')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    if image_file is None:
        return jsonify({"error": "No image provided"}), 400

    return auth_service.register_face_id(email)

# Routes: auth/reset_password
@auth_blueprint.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    return auth_service.reset_password(email)
