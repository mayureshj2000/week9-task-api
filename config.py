import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join("/tmp", "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    RATELIMIT_DEFAULT = "100 per hour"