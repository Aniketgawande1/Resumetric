import os
import json
from flask import Blueprint, request, jsonify, session, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import secrets
import datetime

auth_bp = Blueprint('auth', __name__)

# Simple user storage (replace with database in production)
users_db = {}
reset_tokens = {}  # Store password reset tokens

def get_user_collection():
    """Get MongoDB user collection if available"""
    if hasattr(current_app, 'mongo') and current_app.mongo:
        return current_app.mongo.users
    return None

def store_user(user_data):
    """Store user in database or memory"""
    collection = get_user_collection()
    if collection:
        collection.insert_one(user_data)
    else:
        users_db[user_data['email']] = user_data

def get_user(email):
    """Get user from database or memory"""
    collection = get_user_collection()
    if collection:
        return collection.find_one({"email": email})
    else:
        return users_db.get(email)

def update_user(email, update_data):
    """Update user in database or memory"""
    collection = get_user_collection()
    if collection:
        collection.update_one({"email": email}, {"$set": update_data})
    else:
        if email in users_db:
            users_db[email].update(update_data)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate password strength
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Check if user already exists
        if get_user(email):
            return jsonify({"error": "User already exists"}), 409
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Create user
        user_data = {
            "email": email,
            "name": name,
            "password": password_hash,
            "verified": False,
            "created_at": datetime.datetime.utcnow(),
            "profile_picture": None
        }
        
        store_user(user_data)
        
        # Create JWT token
        access_token = create_access_token(identity=email)
        
        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "access_token": access_token,
            "user": {
                "email": email,
                "name": name,
                "verified": False
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Get user from database
        user = get_user(email)
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Check password
        if not check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=email)
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "email": user['email'],
                "name": user['name'],
                "verified": user.get('verified', False)
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_email = get_jwt_identity()
        user_data = get_user(user_email)
        
        if not user_data:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "user": {
                "email": user_data['email'],
                "name": user_data['name'],
                "verified": user_data.get('verified', False),
                "profile_picture": user_data.get('profile_picture'),
                "created_at": user_data.get('created_at')
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get profile: {str(e)}"}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_email = get_jwt_identity()
        data = request.get_json()
        
        # Get current user
        user = get_user(user_email)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update allowed fields
        update_data = {}
        if data.get('name'):
            update_data['name'] = data['name'].strip()
        if data.get('profile_picture'):
            update_data['profile_picture'] = data['profile_picture']
        
        if update_data:
            update_user(user_email, update_data)
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_email = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({"error": "Current password and new password are required"}), 400
        
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Validate new password strength
        if len(new_password) < 6:
            return jsonify({"error": "New password must be at least 6 characters long"}), 400
        
        # Get user
        user = get_user(user_email)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check current password
        if not check_password_hash(user['password'], current_password):
            return jsonify({"error": "Current password is incorrect"}), 401
        
        # Hash new password
        new_password_hash = generate_password_hash(new_password)
        
        # Update password
        update_user(user_email, {"password": new_password_hash})
        
        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to change password: {str(e)}"}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({"error": "Email is required"}), 400
        
        email = data['email'].lower().strip()
        
        # Check if user exists
        user = get_user(email)
        if not user:
            # Don't reveal if user exists or not
            return jsonify({"message": "If the email exists, a reset link has been sent"}), 200
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        reset_tokens[reset_token] = {
            "email": email,
            "expires_at": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        
        # Send reset email (implement email sending)
        try:
            from flask_mail import Mail
            mail = Mail(current_app)
            
            reset_url = f"http://localhost:3000/reset-password?token={reset_token}"
            
            msg = Message(
                subject="Password Reset - Resumetric",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f"""
            Hello {user['name']},
            
            You requested a password reset. Click the link below to reset your password:
            {reset_url}
            
            This link will expire in 1 hour.
            
            If you didn't request this reset, please ignore this email.
            
            Best regards,
            Resumetric Team
            """
            
            mail.send(msg)
            
        except Exception as e:
            print(f"Failed to send reset email: {e}")
        
        return jsonify({"message": "If the email exists, a reset link has been sent"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to process reset request: {str(e)}"}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token"""
    try:
        data = request.get_json()
        
        if not data.get('token') or not data.get('new_password'):
            return jsonify({"error": "Token and new password are required"}), 400
        
        token = data['token']
        new_password = data['new_password']
        
        # Validate token
        if token not in reset_tokens:
            return jsonify({"error": "Invalid or expired reset token"}), 400
        
        token_data = reset_tokens[token]
        
        # Check if token is expired
        if datetime.datetime.utcnow() > token_data['expires_at']:
            del reset_tokens[token]
            return jsonify({"error": "Reset token has expired"}), 400
        
        # Validate new password
        if len(new_password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Hash new password
        new_password_hash = generate_password_hash(new_password)
        
        # Update password
        update_user(token_data['email'], {"password": new_password_hash})
        
        # Remove used token
        del reset_tokens[token]
        
        return jsonify({
            "success": True,
            "message": "Password reset successfully"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to reset password: {str(e)}"}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user"""
    return jsonify({
        "success": True,
        "message": "Successfully logged out",
        "instructions": "Please remove the JWT token from your client storage"
    })

@auth_bp.route('/verify-token', methods=['POST'])
@jwt_required()
def verify_token():
    """Verify JWT token"""
    try:
        user_email = get_jwt_identity()
        user = get_user(user_email)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "valid": True,
            "user": {
                "email": user['email'],
                "name": user['name'],
                "verified": user.get('verified', False)
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Token verification failed: {str(e)}"}), 500
