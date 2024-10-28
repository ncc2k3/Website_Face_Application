import face_recognition
import numpy as np
import cv2
from app.repositories.UserRepository import UserRepository
from flask import session
from app.packages.auth.models.User import User
from flask import jsonify, request
import uuid
import os
from app.services.BaseService import BaseService
from app.config.AppConfig import Config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AuthService(BaseService):
    def __init__(self):
        super().__init__(User, session)
        self.user_repo = UserRepository()

    ### Hàm đăng ký người dùng
    def register_user(self, first_name, last_name, email, password):
        # Kiểm tra xem email đã được đăng ký chưa
        user = self.user_repo.find_by_email(email)
        
        if user:
            return {"error": "Email already registered"}, 400
        
        # Tạo user mới
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        
        # Lưu user vào database
        self.repository.add(new_user)
        
        return {"message": "User registered successfully"}, 200
    
    ### Hàm đăng kí face ID cho user
    def register_face_id(self, email):
        # Tìm user bằng email
        user = self.user_repo.find_by_email(email)
        
        # Nếu không tìm thấy user
        if not user:
            return jsonify({"message": "User not found"}), 400
        
        image_file = request.files.get('image') 
        if image_file is None:
            return jsonify({"message": "No image provided"}), 400
    
        # Lưu ảnh cho user dựa trên id hoặc email
        image_path = f"./app/images/{uuid.uuid4()}.jpg"  # Có thể thay bằng user.email nếu cần
        image_file.save(image_path)
    
        # Sử dụng face_recognition để tải ảnh trực tiếp thay vì cv2.imread
        image = face_recognition.load_image_file(image_path)
        
        # Lấy face encoding từ ảnh
        encodings = face_recognition.face_encodings(image)

        # Kiểm tra kết quả face_encodings
        if len(encodings) == 0:
            print("No face found in image")
            os.remove(image_path)  # Xóa file nếu không có khuôn mặt
            return jsonify({"message": "No face found in image"}), 400  # Trả về lỗi nếu không có khuôn mặt
        
        face_encoding = encodings[0]  # Lấy face encoding đầu tiên (nếu có nhiều khuôn mặt)
        
        # Lưu face encoding vào DB
        user.face_encoding = face_encoding.tobytes()  # Chuyển encoding sang dạng byte để lưu vào CSDL
        
        # Cập nhật vào database
        self.repository.update()
        
        # Xóa file ảnh sau khi lưu face encoding
        os.remove(image_path)
        
        # Trả về phản hồi thành công
        return jsonify({"message": "Face ID saved successfully"}), 200  # Trả về thành công nếu lưu được face ID

    ### Hàm xác thực người dùng
    def authenticate_user(self, email, password):
        user = self.user_repo.find_by_email(email)
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

        return jsonify({'error': 'Invalid email or password'}), 400
    
    ### Hàm xác thực bằng face ID
    def authenticate_by_face(self, image_file):
        # Tạo tên file ảnh tạm thời dựa trên uuid để tránh ghi đè
        temp_image_path = f"./app/images/{uuid.uuid4()}.jpg"
        image_file.save(temp_image_path)
        
        # Sử dụng face_recognition để tải ảnh trực tiếp 
        image = face_recognition.load_image_file(temp_image_path)

        # Chuyển ảnh về RGB nếu cần (face_recognition sẽ tự động xử lý)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) == 0:
            # print("No face found in image for authentication")
            return {"error": "No face found in image"}, 400
        
        face_encoding = face_encodings[0]
        
        # Lấy tất cả users từ database
        users = User.query.all()
        
        for user in users:
            if user.face_encoding:
                stored_face_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)
                
                # So sánh khuôn mặt
                result = face_recognition.compare_faces([stored_face_encoding], face_encoding)
                
                if result[0]:  # Kết quả so khớp khuôn mặt
                    # Xóa file ảnh tạm sau khi xác thực xong
                    os.remove(temp_image_path)
                    return jsonify({"message": "Login successful", "user": user.email}), 200
        
        # Xóa file ảnh tạm sau khi xác thực xong
        os.remove(temp_image_path)
        
        return jsonify({"message": "Face ID does not match"}), 200
    
    # Hàm quên mật khẩu
    def reset_password(self, email):
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return jsonify({"message": "User not found"}), 400
        
        # Tạo mật khẩu mới
        new_password = Config.SECRET_SET_PASSWORD
        
        print("\n\n new_password:", new_password, "\n\n")
        
        # Cập nhật mật khẩu mới vào database
        user.set_password(new_password)
        self.repository.update()
        
        # Gửi mật khẩu mới đến email người dùng
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
