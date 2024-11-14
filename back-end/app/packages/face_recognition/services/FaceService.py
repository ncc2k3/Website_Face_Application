from deepface import DeepFace
import cv2
import numpy as np
from typing import List


class FaceService:
    def __init__(self):
        self.model = 'SFace'
        self.detector = 'yunet'
        self.distance_metric = 'euclidean_l2'
        # pass

    def detect_faces(self, image_path: str):
        """Detect faces in an image using DeepFace."""
        # Load the image for face detection
        img = cv2.imread(image_path)

        # Use DeepFace's extract_faces function to detect and extract faces
        faces = DeepFace.extract_faces(
            img_path=image_path,  # The image path or image array
            # You can use "opencv", "mtcnn", "retinaface", "dlib", etc.
            detector_backend=self.detector,
            enforce_detection=False,  # If False, it won't raise an error if no faces are found
            anti_spoofing=True,  # Optional: To perform anti-spoofing
        )
        print("face count:", len(faces))
        if not faces:
            return {"message": "No faces detected"}

        return faces  # Returns detected faces along with key points

    def recognize_face(self, image_path: str, db_path: str):
        """Compare a face from an image with a database."""
        # Perform face recognition with DeepFace to find the closest match in the database
        result = DeepFace.find(
            img_path=image_path,  # Path to the image to be recognized
            db_path=db_path,      # Path to the database of known faces
            # You can choose from several models like 'VGG-Face', 'Facenet', 'OpenFace'
            model_name=self.model,
            # You can change to 'euclidean', 'angular', etc.
            distance_metric=self.distance_metric,
            detector_backend=self.detector,
            enforce_detection=False  # Do not enforce face detection (Optional)
        )

        # Return the first match or None if no match found
        if result and len(result) > 0:
            return result[0]
        else:
            return {"message": "No match found"}

    def compare_faces(self, image_path1: str, image_path2: str):
        """Compare two faces to check if they belong to the same person."""
        # Perform face comparison with DeepFace using the 'verify' method
        result = DeepFace.verify(
            image_path1, image_path2, model_name='VGG-Face', distance_metric='cosine')

        # Return the result indicating whether the faces match
        if result["verified"]:
            return {"result": "Faces match!"}
        else:
            return {"result": "Faces do not match!"}

    def search_faces(self, image_path: str, db_path: str):
        """Search for a face in the database."""
        # Perform face search in the database using DeepFace's 'find' function
        result = DeepFace.find(
            img_path=image_path,  # The image to search for
            db_path=db_path,      # The directory containing the known faces
            model_name=self.model,  # Model to use for face recognition
            distance_metric=self.distance_metric,  # The metric used for comparison
            enforce_detection=False
        )

        if result and len(result) > 0:
            return {"closest_match": result[0]}
        else:
            return {"message": "No faces found in the database"}

    def get_embedding(self,image_path:str,db_path:str):
        
        # embedding = DeepFace.
        pass