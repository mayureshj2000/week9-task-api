from app.users import bp
from flask import jsonify

@bp.route("/")
def get_users():
    return jsonify({"message": "Users route working"})