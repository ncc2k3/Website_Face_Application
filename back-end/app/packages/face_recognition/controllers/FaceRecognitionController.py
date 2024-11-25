from flask import Blueprint, request, jsonify
from app.packages.face_recognition.services.FaceRecognitionService import FaceRecognitionService
import os
import uuid

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
    image_path = f"./app/images_tempt/{image_file.filename}"
    image_file.save(image_path)
    
    try:
        # Phát hiện khuôn mặt và trả về tọa độ bounding box
        result = face_recognition_service.detect_faces(image_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Xóa ảnh tạm sau khi xử lý
        os.remove(image_path)

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

    # Tạo tên tệp bằng UUID
    image1_filename = f"{uuid.uuid4()}.jpg"
    image2_filename = f"{uuid.uuid4()}.jpg"

    # Đường dẫn để lưu ảnh tạm
    image1_path = f"./app/images_tempt/{image1_filename}"
    image2_path = f"./app/images_tempt/{image2_filename}"

    # Lưu ảnh tạm
    image1.save(image1_path)
    image2.save(image2_path)

    try:
        # So sánh 2 ảnh và trả về độ giống nhau
        result = face_recognition_service.face_compares(image1_path, image2_path)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Xóa 2 ảnh tạm sau khi xử lý
        if os.path.exists(image1_path):
            os.remove(image1_path)
        if os.path.exists(image2_path):
            os.remove(image2_path)
            
# routes: /face_recognition/liveness
@face_recognition_blueprint.route('/liveness_detection', methods=['POST'])
def liveness_detection():
    """
    Endpoint để kiểm tra liveness của ảnh.
    """
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Tạo tên tệp bằng UUID
    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = f"./app/images_tempt/{image_filename}"

    # Lưu ảnh tạm
    image_file.save(image_path)

    try:
        # Gọi hàm liveness detection
        result, status_code = face_recognition_service.liveness_detection(image_path)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Xóa ảnh tạm sau khi xử lý
        if os.path.exists(image_path):
            os.remove(image_path)


# routes: /face_recognition/search
@face_recognition_blueprint.route('/search', methods=['POST'])
def search_face():
    """
    Endpoint để tìm kiếm khuôn mặt trong cơ sở dữ liệu từ ảnh được gửi.
    """
    # Lấy ảnh từ request
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Lưu ảnh tạm để xử lý
    temp_image_path = f"./app/images_tempt/{uuid.uuid4().hex}.jpg"
    image_file.save(temp_image_path)

    try:
        # Tìm kiếm khuôn mặt trong database
        result = face_recognition_service.search_face(temp_image_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Xóa ảnh tạm sau khi xử lý
        os.remove(temp_image_path)
