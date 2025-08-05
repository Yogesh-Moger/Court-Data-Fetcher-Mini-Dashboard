from flask import Flask
from .routes import main
from .scraper import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.register_blueprint(main)
    init_db()
    return app
