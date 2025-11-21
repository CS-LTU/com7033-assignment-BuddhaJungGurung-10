# In this file, Flask extensions are initialized inorder to keep the application factory function clean and organized.
# This also removes circular import issues by centralizing extension initialization.

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_pymongo import PyMongo


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mongo = PyMongo()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'