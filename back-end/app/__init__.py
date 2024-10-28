from flask import Flask
from app.packages.auth.controllers.AuthController import auth_blueprint
from app.controllers import *
from flask_sqlalchemy import SQLAlchemy
from app.config.Database import userdb
from flask_cors import CORS, cross_origin
from app.config.AppConfig import Config
from app.controllers.hello import index_blueprint

def create_app():
    app = Flask(__name__)
    
    # Cấu hình cho app, bao gồm kết nối database
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    CORS(app,supports_credentials=True)
    
    # Khởi tạo các thành phần mở rộng
    userdb.init_app(app)
    
    with app.app_context():
        # Route index
        app.register_blueprint(index_blueprint)
    
        # Đăng ký các Blueprint hoặc các route khác nếu cần
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        
        # Tạo database nếu cần
        userdb.create_all()

    return app


