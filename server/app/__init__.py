from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
import secrets
from dotenv import load_dotenv

mail = Mail()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    # CORS configuration for Google OAuth
    CORS(app, origins=["http://localhost:3000", "http://localhost:5000"], supports_credentials=True)
    
    # Secret key for sessions
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", secrets.token_hex(16))
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    
    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
    app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")
    
    # Google OAuth configuration
    app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")
    app.config['GOOGLE_REDIRECT_URI'] = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/api/auth/callback")

    # MongoDB setup
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB", "resumetric")
    if mongo_uri:
        try:
            client = MongoClient(mongo_uri)
            app.mongo = client[mongo_db_name]
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            app.mongo = None
    else:
        app.mongo = None

    mail.init_app(app)
    jwt.init_app(app)

    from .auth import auth_bp
    from .routes import routes_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(routes_bp, url_prefix='/api')

    return app
