from flask import Flask
from instance.config import Config
import os


def create_app():
    # Initialize the Flask application
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the configuration from instance/config.py
    app.config.from_object(Config)
    
    # Register the routes from routes.py
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app
