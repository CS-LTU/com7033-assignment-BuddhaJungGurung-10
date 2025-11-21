# configuration settings for the app (e.g., database URIs, secret keys)

import os
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig:
    SECRET_KEY = config("SECRET_KEY", default="flask-insecure-dev-key")
    SQLALCHEMY_DATABASE_URI = config(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "../instance/auth.sqlite"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017/stroke_db")
