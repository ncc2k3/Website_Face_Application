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
    Endpoint to send an image and receive the bounding box coordinates of the faces.
    """
    # Get image from request
    image_file = request.files.get('image')
    
    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Save image temporarily for processing
    image_path = f"./app/images_tempt/{image_file.filename}"
    image_file.save(image_path)
    
    try:
        # Detect face and return bounding box coordinates
        result = face_recognition_service.detect_faces(image_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Delete temporary image after processing
        os.remove(image_path)

# routes: /face_recognition/compare
@face_recognition_blueprint.route('/compare', methods=['POST'])
def compare_faces():
    """
    Endpoint to compare two images and return the similarity between them.
    """
    # Get 2 images from request
    image1 = request.files.get('image1')
    image2 = request.files.get('image2')

    if not image1 or not image2:
        return jsonify({"message": "Two images are required"}), 400

    # Create filename using UUID
    image1_filename = f"{uuid.uuid4()}.jpg"
    image2_filename = f"{uuid.uuid4()}.jpg"

    # Path to save temporary image
    image1_path = f"./app/images_tempt/{image1_filename}"
    image2_path = f"./app/images_tempt/{image2_filename}"

    # Save temporary image
    image1.save(image1_path)
    image2.save(image2_path)

    try:
        # Compare 2 images and return similarity
        result = face_recognition_service.face_compares(image1_path, image2_path)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Delete 2 temporary images after processing
        if os.path.exists(image1_path):
            os.remove(image1_path)
        if os.path.exists(image2_path):
            os.remove(image2_path)
            
# routes: /face_recognition/liveness
@face_recognition_blueprint.route('/liveness_detection', methods=['POST'])
def liveness_detection():
    """
    Endpoint to check the liveness of an image.
    """
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Create filename using UUID
    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = f"./app/images_tempt/{image_filename}"

    # Save temporary image
    image_file.save(image_path)

    try:
        # Call liveness detection function
        result, status_code = face_recognition_service.liveness_detection(image_path)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete temporary image after processing
        os.remove(image_path)


# routes: /face_recognition/search
@face_recognition_blueprint.route('/search', methods=['POST'])
def search_face():
    """
    Endpoint to search for a face in the database from an image sent.
    """
    # Get image from request
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Save image temporarily for processing
    temp_image_path = f"./app/images_tempt/{uuid.uuid4().hex}.jpg"
    image_file.save(temp_image_path)

    try:
        # Search for face in database
        result = face_recognition_service.search_face(temp_image_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Delete temporary image after processing
        os.remove(temp_image_path)

# routes: /face_recognition/search_folder
@face_recognition_blueprint.route('/search_folder', methods=['POST'])
def search_face_folder():
    """
    Endpoint to search for a face in the database from an image sent.
    """
    # Get image from request
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({"message": "No image provided"}), 400

    # Save image temporarily for processing
    temp_image_path = f"./app/images_tempt/{uuid.uuid4().hex}.jpg"
    image_file.save(temp_image_path)

    try:
        # Search for face in database
        folder_path = f"./app/store_database/imgs_database_faces"
        result = face_recognition_service.search_face_in_folder(temp_image_path,folder_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        # Delete temporary image after processing
        os.remove(temp_image_path)
