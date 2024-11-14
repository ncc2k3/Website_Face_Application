from flask import Blueprint, request, jsonify
from app.packages.face_recognition.services.FaceService import FaceService
import os

face_recog_blueprint = Blueprint('face_recognition', __name__)
face_recog_service = FaceService()

# Route: face_recognition/face_detection
@face_recog_blueprint.route('/face_detection', methods=['POST'])
def face_detection():
    image_file = request.files.get('image')
    
    if not image_file:
        return jsonify({"error": "No image provided"}), 400
    
    # Call the face detection method in the service
    try:
        detected_faces = face_recog_service.detect_faces(image_file)
        return jsonify({"faces": detected_faces}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: face_recognition/face_comparison
@face_recog_blueprint.route('/face_comparison', methods=['POST'])
def face_comparison():
    image_file_1 = request.files.get('image_1')
    image_file_2 = request.files.get('image_2')
    
    if not image_file_1 or not image_file_2:
        return jsonify({"error": "Both images are required for comparison"}), 400
    
    # Call the face comparison method in the service
    try:
        comparison_result = face_recog_service.compare_faces(image_file_1, image_file_2)
        return jsonify({"match": comparison_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: face_recognition/face_search
@face_recog_blueprint.route('/face_search', methods=['POST'])
def face_search():
    image_file = request.files.get('image')
    
    if not image_file:
        return jsonify({"error": "No image provided for search"}), 400
    
    # Call the face search method in the service
    try:
        search_results = face_recog_service.search_face(image_file)
        return jsonify({"results": search_results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: face_recognition/anti_spoofing
@face_recog_blueprint.route('/anti_spoofing', methods=['POST'])
def anti_spoofing():
    image_file = request.files.get('image')
    
    if not image_file:
        return jsonify({"error": "No image provided for anti-spoofing detection"}), 400
    
    # Call the anti-spoofing (liveness detection) method in the service
    try:
        spoofing_result = face_recog_service.detect_faces(image_file)
        return jsonify({"is_real": spoofing_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
