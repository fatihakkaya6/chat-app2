from flask import jsonify, request
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User  # Import the User model from models/user_model.py

def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.objects(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"msg": "Incorrect Username or Password", "status": False}), 400
        
        user.password = None  # Remove password from response for security
        return jsonify({"status": True, "user": user.to_json()}), 200
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500

def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.objects(username=username).first():
            return jsonify({"msg": "Username already used", "status": False}), 400
        
        if User.objects(email=email).first():
            return jsonify({"msg": "Email already used", "status": False}), 400
        
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        user.save()
        
        user.password = None  # Remove password from response for security
        return jsonify({"status": True, "user": user.to_json()}), 201
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500

def get_all_users(id):
    try:
        users = User.objects.exclude(id=ObjectId(id)).only('email', 'username', 'avatarImage')
        users_list = [{"email": user.email, "username": user.username, "avatarImage": user.avatarImage} for user in users]
        return jsonify(users_list), 200
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500

def set_avatar(id):
    try:
        data = request.get_json()
        avatar_image = data.get('image')
        
        user = User.objects(id=id).first()
        if not user:
            return jsonify({"msg": "User not found", "status": False}), 404
        
        user.avatarImage = avatar_image
        user.isAvatarImageSet = True
        user.save()
        
        return jsonify({"isSet": user.isAvatarImageSet, "image": user.avatarImage}), 200
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500

def log_out(id):
    try:
        if not id:
            return jsonify({"msg": "User id is required "}), 400
        
        # Remove user from onlineUsers
        if id in online_users:
            del online_users[id]
        
        return jsonify({"msg": "User logged out successfully"}), 200
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500
