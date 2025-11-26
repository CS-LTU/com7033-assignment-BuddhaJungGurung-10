import os
from flask import Flask
from .logger import configure_logging
from .config import DefaultConfig
from .extensions import db, login_manager, csrf, mongo
from .auth import bp as auth_bp
from .home import bp as home_bp


def create_app(test_config=None):
    """main application factory function that creates and configures the flask app."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(DefaultConfig)

    if test_config:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    configure_logging(app)
    app.logger.info("Application has started.")

    db.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        try:
            mongo.cx.server_info()  # checking mongodb connection and getting server info
            app.logger.info("Connected to MongoDB successfully.")
        except Exception as e:
            app.logger.error(f"Failed to connect to MongoDB: {e}")
        db.create_all()
        app.logger.info("Database tables created/verified.")

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    # error handlers for not found and internal server error
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"404 error: {error}")
        return "This page does not exist", 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 error: {error}")
        return "An internal error occurred", 500

    return app
