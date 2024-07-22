from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from database import database
from models.user import User

bp = Blueprint("login", __name__)

# Authenticate a user and return a JWT token.
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = database.session.execute(database.select(User).filter_by(username=username)).scalars().first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        return jsonify({"msg": "Authentication Success", "token": token}), 200
    
    return jsonify({"msg": "Authentication Failure"}), 403