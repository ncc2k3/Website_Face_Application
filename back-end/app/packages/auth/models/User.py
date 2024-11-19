from flask_bcrypt import check_password_hash, generate_password_hash

class User:
    __tablename__ = "users"
    
    def __init__(self, id=None, first_name=None, last_name=None, email=None, password=None, face_encoding=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.face_encoding = face_encoding

    def to_insert_query(self):
        query = '''
            INSERT INTO users (first_name, last_name, email, password, face_encoding)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        '''
        values = (self.first_name, self.last_name, self.email, self.password, self.face_encoding)
        return query, values
    
    def to_update_query(self, update_values):
        set_clause = ', '.join([f"{key} = %s" for key in update_values.keys()])
        query = f'''
            UPDATE users SET {set_clause} WHERE email = %s;
        '''
        values = list(update_values.values()) + [self.email]
        return query, values

    def set_password(self, password):
        """Mã hóa mật khẩu và lưu vào thuộc tính `password`"""
        self.password = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        """So sánh mật khẩu đã nhập với mật khẩu đã mã hóa trong cơ sở dữ liệu"""
        return check_password_hash(self.password, password)
