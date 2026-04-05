from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from app.auth import bp
from app.extensions import db
from app.models import User
from app.utils.responses import success_response, error_response
from sqlalchemy import inspect

@bp.post("/register", methods=["POST"])
def register():
    inspector = inspect(db.engine)
    if "user" not in inspector.get_table_names():
        db.create_all()

    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return error_response("username, email and password are required", 400)

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return error_response("User with that username or email already exists", 400)

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)

    return success_response(
        {
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
            },
            "access_token": access,
            "refresh_token": refresh,
        },
        201,
    )

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("email and password are required", 400)

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return error_response("Invalid credentials", 401)

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)

    return success_response(
        {
            "message": "Login successful",
            "access_token": access,
            "refresh_token": refresh,
        }
    )

@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    access = create_access_token(identity=user_id)
    return success_response({"access_token": access})