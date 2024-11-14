from flask import Flask
from app.packages.auth.controllers.AuthController import auth_blueprint
from app.packages.face_recognition.controllers.FaceRecognitionController import face_recognition_blueprint
from app.controllers import *
from flask_cors import CORS
from app.config.AppConfig import Config
from app.controllers.hello import index_blueprint

def create_app():
    app = Flask(__name__)
    
    # Cấu hình cho app
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    # Kích hoạt CORS
    CORS(app, supports_credentials=True)
    
    with app.app_context():
        # Route index
        app.register_blueprint(index_blueprint)
    
        # Đăng ký các Blueprint hoặc các route khác nếu cần
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        
        app.register_blueprint(face_recognition_blueprint, url_prefix='/face_recognition')
    
    return app
