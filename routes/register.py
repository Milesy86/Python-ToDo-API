from flask import Blueprint, request, jsonify
from models.user import User
from database import database

bp = Blueprint("register", __name__)

# Register a new user.
@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
      
    if database.session.execute(database.select(User).filter_by(username=username)).scalars().first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    database.session.add(new_user)
    database.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201