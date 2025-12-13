from flask import Flask
import os

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    templates_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    app.config['SECRET_KEY'] = 'dev'

    from .routes import bp
    app.register_blueprint(bp)
    return app
