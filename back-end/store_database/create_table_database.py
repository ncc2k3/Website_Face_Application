import psycopg2
from flask_bcrypt import Bcrypt

# Tạo đối tượng Bcrypt
bcrypt = Bcrypt()

# Cấu hình kết nối PostgreSQL
db_config = {
    "dbname": "your_database_name",  # Thay tên database
    "user": "your_username",         # Thay username PostgreSQL
    "password": "your_password",     # Thay password PostgreSQL
    "host": "localhost",             # Host
    "port": "5432"                   # Cổng PostgreSQL (mặc định: 5432)
}

# Kết nối tới PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Kết nối thành công tới PostgreSQL!")
except Exception as e:
    print(f"Lỗi kết nối: {e}")
    exit()

# Tạo bảng Users
try:
    cursor.execute("""
    DROP TABLE IF EXISTS Faces CASCADE;
    DROP TABLE IF EXISTS Users CASCADE;
    
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(256) NOT NULL,  -- Lưu mật khẩu đã mã hóa
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Bảng Users đã được tạo!")
except Exception as e:
    print(f"Lỗi tạo bảng Users: {e}")

# Tạo bảng Faces
try:
    cursor.execute("""
    CREATE TABLE Faces (
        face_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
        image_name VARCHAR(255) NOT NULL,
        image_path VARCHAR(255) NOT NULL,
        embedding JSONB NOT NULL, -- Lưu trữ embeddings dạng JSON
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Bảng Faces đã được tạo!")
except Exception as e:
    print(f"Lỗi tạo bảng Faces: {e}")

# Đóng kết nối
cursor.close()
conn.close()
print("Cơ sở dữ liệu đã được thiết lập xong.")
