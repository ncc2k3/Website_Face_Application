from flask import Blueprint, request, jsonify
from app.packages.face_recognition.services.FaceRecognitionService import FaceRecognitionService
import os

face_recognition_blueprint = Blueprint('face_recognition', __name__)
face_recognition_service = FaceRecognitionService()

# routes: /face_recognition/detect
@face_recognition_blueprint.route('/detect', methods=['POST'])
def detect_face():
    """
    Endpoint để client gửi ảnh và nhận lại tọa độ bounding box của các khuôn mặt.
    """
    # Lấy ảnh từ request
    image_file = request.files.get('image')
    
    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Lưu ảnh tạm để xử lý
    image_path = f"./app/images/{image_file.filename}"
    image_file.save(image_path)

    # Phát hiện khuôn mặt và trả về tọa độ bounding box
    result = face_recognition_service.detect_faces(image_path)

    # Xóa ảnh tạm sau khi xử lý
    os.remove(image_path)
    
    return jsonify(result)
