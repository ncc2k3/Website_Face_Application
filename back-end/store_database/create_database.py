import os
import psycopg2
from flask_bcrypt import Bcrypt
from faker import Faker
from deepface import DeepFace
import json

# Cấu hình kết nối PostgreSQL
db_config = {
    'dbname': 'cv_project',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Đường dẫn tới folder chứa ảnh
image_folder = os.path.join(os.getcwd(), 'store_database', 'imgs_database_faces')

# Tạo đối tượng Flask-Bcrypt và Faker
bcrypt = Bcrypt()
faker = Faker()

# Kết nối tới PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Kết nối thành công tới PostgreSQL!")
except Exception as e:
    print(f"Lỗi kết nối: {e}")
    exit()

# Lấy link hiện tại
# Lấy danh sách hình ảnh từ folder
def get_images_from_folder(folder_path):
    """Lấy danh sách file hình ảnh trong folder."""
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Tạo mật khẩu băm
def hash_password(password):
    """Hàm băm mật khẩu bằng flask-bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Thêm user vào bảng Users
def add_user(first_name, last_name, email, password):
    """Thêm một user vào bảng Users."""
    cursor.execute("""
    INSERT INTO Users (first_name, last_name, email, password)
    VALUES (%s, %s, %s, %s) RETURNING user_id;
    """, (first_name, last_name, email, password))
    conn.commit()
    return cursor.fetchone()[0]

# Thêm khuôn mặt vào bảng Faces
def add_face(user_id, image_name, image_path, embedding):
    """Thêm một khuôn mặt vào bảng Faces."""
    cursor.execute("""
    INSERT INTO Faces (user_id, image_name, image_path, embedding)
    VALUES (%s, %s, %s, %s);
    """, (user_id, image_name, image_path, json.dumps(embedding)))
    conn.commit()

# Tạo dữ liệu từ hình ảnh
def create_data_from_images(folder_path):
    """Tạo dữ liệu từ hình ảnh và thêm vào cơ sở dữ liệu."""
    image_paths = get_images_from_folder(folder_path)
    for image_path in image_paths:
        try:
            # Tạo thông tin user ngẫu nhiên
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            password = hash_password("123")

            # Thêm user vào bảng
            user_id = add_user(first_name, last_name, email, password)

            # Xử lý embedding từ ảnh
            image_name = os.path.basename(image_path)
            embedding = DeepFace.represent(img_path=image_path, model_name="SFace")[0]["embedding"]

            # Thêm khuôn mặt vào bảng Faces
            add_face(user_id, image_name, image_path, embedding)
            print(f"Thêm thành công: {image_name} -> User ID: {user_id}")

        except Exception as e:
            print(f"Lỗi xử lý {image_path}: {e}")

# Thực hiện các bước
try:
    create_data_from_images(image_folder)
except Exception as e:
    print(f"Lỗi: {e}")
finally:
    cursor.close()
    conn.close()
    print("Đã đóng kết nối tới PostgreSQL.")
