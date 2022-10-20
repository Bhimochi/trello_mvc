from flask import Flask
from db import db, ma
from controllers.cards_controller import cards_bp
import os

def create_app():
    app = Flask(__name__)

    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(cards_bp)

    @app.route('/')
    def index():
        return 'Hello'
    
    return app