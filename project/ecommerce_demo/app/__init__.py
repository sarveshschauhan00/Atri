from flask import Flask
from flask_session import Session
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'session_files')
    app.config['SESSION_PERMANENT'] = False

    # Ensure the session directory exists
    if not os.path.exists(app.config['SESSION_FILE_DIR']):
        os.makedirs(app.config['SESSION_FILE_DIR'])

    # Initialize session
    Session(app)

    # Import routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
