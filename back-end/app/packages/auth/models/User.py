from app.config.Database import userdb
from flask_bcrypt import generate_password_hash, check_password_hash
import face_recognition
from sqlalchemy import LargeBinary
import numpy as np
import faiss

# FAISS index và user mapping
dimension = 128  # Độ chiều của face_encoding
faiss_index = faiss.IndexFlatL2(dimension)  # Sử dụng L2 distance
user_mapping = {}  # Để map FAISS index với user_id


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

    # Set face_encoding và lưu vào FAISS
    def set_face_encoding(self, face_encoding):
        self.face_encoding = face_encoding.tobytes()  # Lưu dưới dạng nhị phân
        self.add_face_to_faiss(face_encoding)

    # Hàm thêm encoding vào FAISS index
    @staticmethod
    def add_face_to_faiss(face_encoding, user_id):
        global faiss_index, user_mapping
        face_vector = np.array(face_encoding, dtype=np.float32).reshape(1, -1)
        faiss_index.add(face_vector)
        user_mapping[faiss_index.ntotal - 1] = user_id  # Liên kết FAISS index với user_id