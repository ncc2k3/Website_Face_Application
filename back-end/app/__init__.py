from flask import Flask
from app.packages.auth.controllers.AuthController import auth_blueprint
from app.packages.face_recognition.controllers.FaceController import face_recog_blueprint
from app.controllers import *
from flask_sqlalchemy import SQLAlchemy
from app.config.Database import userdb
from flask_cors import CORS
from app.config.AppConfig import Config
from app.controllers.hello import index_blueprint

def create_app():
    app = Flask(__name__)
    
    # Configure the app, including database connections
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    # Initialize CORS with credential support
    CORS(app, supports_credentials=True)
    
    # Initialize database extensions
    userdb.init_app(app)
    # facedb.init_app(app)
    
    with app.app_context():
        # Register the index route
        app.register_blueprint(index_blueprint)
    
        # Register other Blueprints or routes as needed
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(face_recog_blueprint, url_prefix='/face_recognition')
        
        # Create databases if needed
        userdb.create_all()
        # facedb.create_all()  # Ensure facedb tables are also created

    return app
