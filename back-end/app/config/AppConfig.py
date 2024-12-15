import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = os.getenv('PORT')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    
    # Thông tin kết nối
    DATABASE_CONFIG = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    
    # Email và password của người gửi 
    # Lưu ý nhập vào ở file .env
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    
    SECRET_SET_PASSWORD = os.getenv('SECRET_SET_PASSWORD')
