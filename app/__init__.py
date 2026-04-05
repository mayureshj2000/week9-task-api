from flask import Flask, jsonify
from config import Config
from app.extensions import db, migrate, jwt, limiter
from app.utils.responses import error_response

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # limiter.init_app(app)

    with app.app_context():     db.create_all()

    from app.auth import bp as auth_bp
    from app.tasks import bp as tasks_bp
    from app.users import bp as users_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    @app.errorhandler(404)
    def not_found(error):
        return error_response("Not found", 404)

    @app.errorhandler(400)
    def bad_request(error):
        return error_response("Bad request", 400)

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return error_response("Too many requests", 429)

    return app