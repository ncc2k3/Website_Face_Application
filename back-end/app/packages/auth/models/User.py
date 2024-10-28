from app.config.Database import userdb
from flask_bcrypt import generate_password_hash, check_password_hash
import face_recognition
from sqlalchemy import LargeBinary

class User(userdb.Model):
    first_name = userdb.Column(userdb.String(150), nullable=False)
    last_name = userdb.Column(userdb.String(150), nullable=False)
    id = userdb.Column(userdb.Integer, primary_key=True)
    email = userdb.Column(userdb.String(150), unique=True, nullable=False)
    password = userdb.Column(userdb.String(150), nullable=False)
    face_encoding = userdb.Column(LargeBinary)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # Mã hóa mật khẩu trước khi lưu vào DB
        self.set_password(password)

    # Kiểm tra mật khẩu
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    # Set password
    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf8')