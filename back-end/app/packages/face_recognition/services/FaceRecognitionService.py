import cv2
from deepface import DeepFace
from app.config.Database import get_connection
from scipy.spatial.distance import cosine
import numpy as np
import base64
import os
import faiss

class FaceRecognitionService:
    def __init__(self):
        self.detector = 'opencv'  # Use YuNet as detector in DeepFace
        self.model = 'SFace'  # Use SFace model in DeepFace
        self.faiss_index = None
        self.face_id_map = {} # Store mapping between FAISS index and face_id
        
    def build_faiss_index(self):
        """
        Create FAISS index from database embeddings.
        """
        db_embeddings = self.get_embeddings_from_db()
        embeddings = np.array([item["embedding"] for item in db_embeddings]).astype('float32')

        # Normalize all embedding vectors
        faiss.normalize_L2(embeddings)

        # Create FAISS index with Inner Product for cosine similarity
        self.faiss_index = faiss.IndexFlatIP(embeddings.shape[1])  # Inner Product (IP)
        self.faiss_index.add(embeddings)

        # Store mapping between FAISS index and face_id
        self.face_id_map = {i: item["face_id"] for i, item in enumerate(db_embeddings)}
    
    """ ==================== detect faces ==================== """    
    def detect_faces(self, image_path):
        """
        Detect faces in image and return list of bounding boxes.
        """
        # Load image from path
        img = cv2.imread(image_path)

        # Use DeepFace to detect faces
        faces = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend=self.detector,
            enforce_detection = False,  # Don't require face detection if image already contains face
            align = True
        )

        # Check if no face detected
        if not faces:
            return {"message": "No faces detected"}, 400

        # Create list of bounding boxes from detection results
        bounding_boxes = []
        for face in faces:
            box = face["facial_area"]  # Get bounding box coordinates
            bounding_boxes.append({
                "x": int(box["x"]),
                "y": int(box["y"]),
                "width": int(box["w"]),
                "height": int(box["h"])
            })

        confidences = []
        for face in faces:
            confidences.append(face["confidence"])
            
        return {"faces": bounding_boxes, 'confidences': confidences}

    """ ==================== face compares ==================== """    
    def face_compares(self, image1_path, image2_path):
        """
        Compare 2 images and return similarity between them.
        """
        # Use DeepFace to compare 2 images
        try:
            result = DeepFace.verify(
                image1_path,
                image2_path,
                model_name='SFace',
                detector_backend=self.detector,
                # metric: cosine, euclidean, euclidean_l2
                distance_metric='cosine',
                enforce_detection=True # Require face detection before comparison
            )

            # Return comparison result
            return {
                "verified": result["verified"],
                "distance": result["distance"],
                'threshold': result['threshold'],
            }
        except Exception as e:
            # Return error if there's an issue during comparison
            return {"error": str(e)}, 400
        
    """ ==================== liveness detection ==================== """
    def liveness_detection(self, image_path):
        """
        Check liveness and anti-spoofing from input image.
        """
        try:
            # Check if image is valid
            img = cv2.imread(image_path)
            
            if img is None:
                raise ValueError("Image could not be loaded. Check the file path.")

            # Call extract_faces function to analyze face
            faces = DeepFace.extract_faces(
                img_path=image_path,
                detector_backend=self.detector,  # Face detector (opencv, mtcnn, ...)
                # enforce_detection=True,          # Force face detection
                anti_spoofing=True               # Enable anti-spoofing check
            )

            # If no face detected
            if not faces:
                return {"message": "No faces detected", "liveness": False, "spoofing": None}, 400

            # Iterate through detected faces
            results = []
            for face in faces:
                is_real = face.get("is_real", None)  # Anti-spoofing status
                spoof_score = face.get("antispoof_score", None)  # Anti-spoofing score
                confidence = face.get("confidence", None)  # Face detection confidence

                # If result is valid, return status
                results.append({
                    "confidence": confidence,
                    "liveness": is_real,
                    "spoofing_score": spoof_score # True - score- 0.99
                })
            return {"message": "Liveness detection completed", "results": results}, 200

        except Exception as e:
            return {"error": str(e)}, 400

    """ ==================== face seacrh ==================== """
    def get_embeddings_from_db(self):
        """
        Retrieve embeddings from PostgreSQL database.
        faiss - add - delete (exit)
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT face_id, user_id, embedding FROM Faces;")
            data = cursor.fetchall()

            # Convert embedding JSON to numpy array
            embeddings = [
                {
                    "face_id": row[0],
                    "user_id": row[1],
                    "embedding": np.array(row[2])  # Embedding as numpy array
                }
                for row in data
            ]
            return embeddings
        finally:
            cursor.close()
            conn.close()

    def extract_embedding(self, image_path):
        """
        Create embedding from input image using DeepFace.
        """
        try:
            embeddings = DeepFace.represent(
                img_path=image_path,
                model_name=self.model,
                detector_backend=self.detector,
                enforce_detection=True
            )
            if not embeddings:
                return None
            return embeddings[0]["embedding"]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def search_face(self, image_path):
        """
        Search for face in database using FAISS.
        """
        try:
            # Create embedding for query image
            query_embedding = self.extract_embedding(image_path)
            if query_embedding is None:
                return {"matched": False, "message": "No face detected in the image"}

            if self.faiss_index is None:
                self.build_faiss_index()

            # Normalize query embedding
            query_embedding = np.expand_dims(query_embedding, axis=0).astype('float32')
            faiss.normalize_L2(query_embedding)

            # Find nearest neighbor
            distances, indices = self.faiss_index.search(query_embedding, k=1)

            # Get best result
            best_index = indices[0][0]
            similarity = float(distances[0][0])  # Convert numpy.float32 to float
            best_face_id = self.face_id_map[best_index]

            # Retrieve face information from database
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT user_id, image_path FROM Faces WHERE face_id = %s;", (best_face_id,))
                row = cursor.fetchone()
                user_id, image_path_db = row

                if not os.path.exists(image_path_db):
                    return {"matched": False, "message": "Image file does not exist in database"}

                with open(image_path_db, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

                return {
                    "matched": True,
                    "similarity": similarity,  # Converted to float type
                    "user_id": user_id,
                    "image_base64": encoded_image
                }
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            return {"matched": False, "message": str(e)}
        
    #####################################
    def build_faiss_index_from_folder(self, folder_path):
        """
        Create FAISS index from images in a folder.
        """
        try:
            embeddings = []
            self.face_id_map = {}

            # Iterate through all image files in folder
            for i, filename in enumerate(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    embedding = self.extract_embedding(file_path)
                    if embedding is not None:
                        embeddings.append(embedding)
                        self.face_id_map[i] = file_path  # Store index -> file path mapping

            # If no embeddings, return error
            if not embeddings:
                raise ValueError("No valid faces found in the folder.")

            embeddings = np.array(embeddings).astype('float32')
            faiss.normalize_L2(embeddings)

            # Create FAISS index IVF
            dim = embeddings.shape[1]
            nlist = 10  # Number of clusters
            quantizer = faiss.IndexFlatL2(dim)  # Use L2 quantizer (or can use IndexFlatIP)
            self.faiss_index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_L2)

            # Train IVF index
            if not self.faiss_index.is_trained:
                print(f"Training FAISS index with {embeddings.shape[0]} samples...")
                self.faiss_index.train(embeddings)

            # Add embeddings to index
            print("Adding embeddings to FAISS index...")
            self.faiss_index.add(embeddings)

            return {"message": "FAISS index built successfully from folder."}
        except Exception as e:
            return {"error": str(e)}

    def search_face_in_folder(self, image_path, folder_path):
        """
        Search for face in a folder and return list of 5 matching images with similarity scores.
        """
        try:
            # Check and update FAISS index if needed
            if self.faiss_index is None or not self.face_id_map:
                self.build_faiss_index_from_folder(folder_path)

            # Create embedding for query image
            query_embedding = self.extract_embedding(image_path)
            if query_embedding is None:
                return {"matched": False, "message": "No face detected in the query image."}

            query_embedding = np.expand_dims(query_embedding, axis=0).astype('float32')
            faiss.normalize_L2(query_embedding)

            # Find nearest neighbors (Top K)
            k = 5  # Number of results to return
            nprobe = 5  # Number of clusters to search in FAISS (usually less than or equal to nlist)
            self.faiss_index.nprobe = nprobe
            distances, indices = self.faiss_index.search(query_embedding, k=k)
            print("\n\n\Indices:", indices)
            # Initialize result list
            encoded_images = []
            similarities = []

            # Iterate through returned results
            for i, index in enumerate(indices[0]):
                file_path = self.face_id_map.get(index, None)
                similarity = float(distances[0][i])

                # Skip if file doesn't exist
                if file_path is None or not os.path.exists(file_path):
                    continue

                # Read and encode image
                with open(file_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
                    encoded_images.append(encoded_image)
                    similarities.append(similarity)

            if not encoded_images:
                return {"matched": False, "message": "No matching faces found or files missing."}

            return {
                "matched": True,
                "encoded_images": encoded_images,
                "similarities": similarities
            }

        except Exception as e:
            return {"matched": False, "message": str(e)}