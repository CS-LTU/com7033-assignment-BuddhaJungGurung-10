import os
import logging
from flask import Flask

def configure_logging(app: Flask):
    """Simple logging setup for the flask application."""
    
    os.makedirs("logs", exist_ok=True)

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # File
    file = logging.FileHandler("logs/app.log")
    file.setFormatter(formatter)

    # Configure app logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(console)
    app.logger.addHandler(file)
    app.logger.propagate = False

    # Optional: HTTP requests
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.handlers = [console, file]
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.propagate = False

    app.logger.info("Logging configured")
