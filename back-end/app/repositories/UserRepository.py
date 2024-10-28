from app.packages.auth.models.User import User
from app.repositories.BaseRepository import BaseRepository
from flask import session

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User, session) # Gọi hàm khởi tạo của BaseRepository và truyền vào model User
    
    def find_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
    def find_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
