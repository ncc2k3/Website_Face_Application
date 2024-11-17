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

# routes: /face_recognition/compare
@face_recognition_blueprint.route('/compare', methods=['POST'])
def compare_faces():
    """
    Endpoint để so sánh 2 ảnh và trả về độ giống nhau giữa chúng.
    """
    # Lấy 2 ảnh từ request
    image1 = request.files.get('image1')
    image2 = request.files.get('image2')

    if not image1 or not image2:
        return jsonify({"message": "Two images are required"}), 400

    # Lưu 2 ảnh tạm để xử lý
    image1_path = f"./app/images/{image1.filename}"
    image2_path = f"./app/images/{image2.filename}"
    image1.save(image1_path)
    image2.save(image2_path)

    # So sánh 2 ảnh và trả về độ giống nhau
    result = face_recognition_service.compare_faces(image1_path, image2_path)

    # Xóa 2 ảnh tạm sau khi xử lý
    os.remove(image1_path)
    os.remove(image2_path)

    return jsonify(result)
