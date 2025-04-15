import os
import uuid
import numpy as np
from flask import session, jsonify, request
from app.repositories.UserRepository import UserRepository
from app.packages.auth.models.User import User
from app.services.BaseService import BaseService
from app.config.AppConfig import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class AuthService(BaseService):
    def __init__(self):
        super().__init__(User)
        self.user_repo = UserRepository()

    ### User registration function
    def register_user(self, first_name, last_name, email, password):
        user = self.user_repo.find_by_email(email)
        if user:
            return {"error": "Email already registered"}, 400
        
        # Create new user and hash password
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=None
        )
        new_user.set_password(password)

        # Save user to Users table
        self.user_repo.add_user(new_user)
        return {"message": "User registered successfully"}, 200

    def register_face_id(self, email):
        user = self.user_repo.find_by_email(email)
        if not user:
            return {"error": "User not found"}, 400

        image_file = request.files.get('image')
        if not image_file:
            return {"error": "No image provided"}, 400

        # Save temporary image
        image_directory = "./store_database/imgs_database_faces"
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)

        image_path = os.path.join(image_directory, f"{uuid.uuid4()}.jpg")
        try:
            image_file.save(image_path)

            # Use FaceRecognitionService to create embedding
            from app.packages.face_recognition.services.FaceRecognitionService import FaceRecognitionService
            face_recognition_service = FaceRecognitionService()
            embedding = face_recognition_service.extract_embedding(image_path)

            if embedding is None:
                return {"error": "No face found in image"}, 400

            # Save embedding and image path to database
            self.user_repo.add_face(
                user_id=user.user_id,
                image_name=os.path.basename(image_path),
                image_path=image_path,
                embedding=embedding
            )
            return {"message": "Face ID registered successfully"}, 200

        except Exception as e:
            print(f"Error registering face ID: {e}")
            return {"error": str(e)}, 500


    ### Login with email and password function
    def authenticate_user(self, email, password):
        user = self.user_repo.find_by_email(email)
        if user and user.check_password(password):
            session['user_id'] = user.user_id
            return jsonify({
                "message": "Login successful",
                "user_id": user.user_id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }), 200

        return {"error": "Invalid email or password"}, 400

    ### Login with Face ID function
    def authenticate_by_face(self, image_file):
        temp_image_path = f"./app/images_tempt/{uuid.uuid4()}.jpg"
        try:
            image_file.save(temp_image_path)
            print(f"Temp image saved: {temp_image_path}")

            from app.packages.face_recognition.services.FaceRecognitionService import FaceRecognitionService
            face_recognition_service = FaceRecognitionService()
            search_result = face_recognition_service.search_face(temp_image_path)

            print("Search result:", search_result)
            if search_result["matched"]:
                user = self.user_repo.find_by_user_id(search_result["user_id"])
                if user:
                    return jsonify({
                        "message": "Login successful",
                        "user_id": user.user_id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "confidence": search_result["similarity"],
                        "matched_image": search_result["image_base64"]
                    }), 200
            return {"error": "Face ID does not match"}, 400

        except Exception as e:
            print(f"Error authenticating face: {e}")
            return {"error": str(e)}, 500

        finally:
            os.remove(temp_image_path)

    ### Reset password function
    def reset_password(self, email):
        user = self.user_repo.find_by_email(email)
        if not user:
            return {"error": "User not found"}, 400

        # Create new password and send via email
        new_password = str(uuid.uuid4())[:8]
        user.set_password(new_password)
        self.user_repo.update_user(user, {"password": user.password})

        # Send email
        self.send_email(email, "Reset Password", f"Your new password is: {new_password}")
        return {"message": "New password sent to your email"}, 200

    ### Send email function
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
