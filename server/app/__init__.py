from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from dotenv import load_dotenv

mail = Mail()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
    app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")

    # ✅ Proper MongoDB setup
    mongo_uri = os.getenv("MONGO_URI")  # must include cluster and credentials
    mongo_db_name = os.getenv("MONGO_DB")  # e.g., "resumetric"
    client = MongoClient(mongo_uri)
    app.mongo = client[mongo_db_name]  # ✅ This avoids get_default_database()

    mail.init_app(app)
    jwt.init_app(app)

    from .auth import auth_bp
    from .routes import routes_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(routes_bp, url_prefix='/api')

    return app
