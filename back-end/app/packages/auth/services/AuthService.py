import face_recognition
import numpy as np
import uuid
import os
import smtplib
from flask import session, jsonify, request
from app.repositories.UserRepository import UserRepository
from app.packages.auth.models.User import User
from app.services.BaseService import BaseService
from app.config.AppConfig import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AuthService(BaseService):
    def __init__(self):
        super().__init__(User)  # Không cần truyền session vào BaseService
        self.user_repo = UserRepository()  # Sử dụng UserRepository trực tiếp

    def register_user(self, first_name, last_name, email, password):
        user = self.user_repo.find_by_email(email)
        print("password login: ", password)
        if user:
            return {"error": "Email already registered"}, 400
        
        # Tạo user mới và mã hóa mật khẩu trước khi lưu
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=None)
        new_user.set_password(password)  # Mã hóa mật khẩu trước khi lưu
        
        print("new_user", new_user.password)
        # Lưu user vào database
        self.user_repo.add_user(new_user)
        
        return {"message": "User registered successfully"}, 200
    
    ### Hàm đăng kí face ID cho user
    def register_face_id(self, email):
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return jsonify({"message": "User not found"}), 400
        
        image_file = request.files.get('image') 
        if not image_file:
            return jsonify({"message": "No image provided"}), 400
    
        image_path = f"./app/images/{uuid.uuid4()}.jpg"
        image_file.save(image_path)
    
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            os.remove(image_path)
            return jsonify({"message": "No face found in image"}), 400
        
        face_encoding = encodings[0]
        user.face_encoding = face_encoding.tobytes()
        
        # Cập nhật vào database
        self.user_repo.update_user(user, {"face_encoding": user.face_encoding})
        
        os.remove(image_path)
        return jsonify({"message": "Face ID saved successfully"}), 200

    ### Hàm xác thực người dùng
    def authenticate_user(self, email, password):
        user = self.user_repo.find_by_email(email)
        # print("password login face: ", password)
        # print("user password face", user.password)
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful', 'user_id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}), 200

        return jsonify({'error': 'Invalid email or password'}), 400
    
    ### Hàm xác thực bằng face ID
    def authenticate_by_face(self, image_file):
        temp_image_path = f"./app/images/{uuid.uuid4()}.jpg"
        image_file.save(temp_image_path)
        
        image = face_recognition.load_image_file(temp_image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) == 0:
            return {"error": "No face found in image"}, 400
        
        face_encoding = face_encodings[0]
        users = self.user_repo.get_all_users()
        
        for user in users:
            if user.face_encoding:
                stored_face_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)
                result = face_recognition.compare_faces([stored_face_encoding], face_encoding)
                
                if result[0]:  
                    os.remove(temp_image_path)
                    return jsonify({"message": "Login successful", "user": user.email, 'first_name': user.first_name, 'last_name': user.last_name}), 200
        
        os.remove(temp_image_path)
        return jsonify({"message": "Face ID does not match"}), 400
    
    # Hàm quên mật khẩu
    def reset_password(self, email):
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return jsonify({"message": "User not found"}), 400
        
        new_password = Config.SECRET_SET_PASSWORD
        user.set_password(new_password)
        self.user_repo.update_user(user, {"password": user.password})
        
        self.send_email(email, "Reset Password", f"Your new password is: {new_password}")
        
        return jsonify({"success": True, "message": "New password sent to your email"}), 200

    ### Hàm gửi email
    @staticmethod
    def send_email(to_email, subject, body):
        sender_email = Config.SENDER_EMAIL
        sender_password = Config.SENDER_PASSWORD
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}")

        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")

        finally:
            server.quit()
