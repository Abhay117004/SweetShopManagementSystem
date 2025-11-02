import os
from flask import Flask
from flask_cors import CORS
from database import db


def create_app():
    app = Flask(__name__)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-User-ID"]
        }
    })

    database_uri = os.environ.get('DATABASE_URL', 'sqlite:///sweetshop.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-change-in-production')

    db.init_app(app)

    from routes import bp
    app.register_blueprint(bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
        from models import Sweet
        if Sweet.query.count() == 0:
            seed_initial_data()

    return app


def seed_initial_data():
    """Initialize database with sample data (removed - data is user-specific now)"""
    pass


app = create_app()


def handler(event, context):
    """Serverless function handler for deployment platforms"""
    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
