from app.repositories.BaseRepository import BaseRepository
from app.config.Database import get_connection
from app.packages.auth.models.User import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    # Tìm user theo email
    def find_by_email(self, email):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Đảm bảo thứ tự cột đúng: id, first_name, last_name, email, password, face_encoding
                cursor.execute("SELECT id, first_name, last_name, email, password, face_encoding FROM users WHERE email = %s", (email,))
                user_data = cursor.fetchone()
                if user_data:
                    # Khởi tạo User với đúng thứ tự giá trị
                    return User(*user_data)
                return None

    # Thêm user mới
    def add_user(self, user_instance):
        query, values = user_instance.to_insert_query()
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                user_instance.id = cursor.fetchone()[0]  # PostgreSQL tự động gán id mới
                conn.commit()
                
    # Cập nhật user
    def update_user(self, instance, update_values):
        query, values = instance.to_update_query(update_values)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
    
    """Lấy tất cả người dùng từ cơ sở dữ liệu"""
    def get_all_users(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, first_name, last_name, email, password, face_encoding FROM users")
                users_data = cursor.fetchall()
                # Trả về danh sách các đối tượng User
                return [User(*user_data) for user_data in users_data]