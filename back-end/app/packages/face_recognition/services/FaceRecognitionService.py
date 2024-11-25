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
        self.detector = 'opencv'  # Sử dụng YuNet làm detector trong DeepFace
        self.model = 'SFace'  # Sử dụng SFace model trong DeepFace
        self.faiss_index = None
        self.face_id_map = {} # Lưu ánh xạ giữa FAISS index và face_id
        
    def build_faiss_index(self):
        """
        Tạo FAISS index từ cơ sở dữ liệu embedding.
        """
        db_embeddings = self.get_embeddings_from_db()
        embeddings = np.array([item["embedding"] for item in db_embeddings]).astype('float32')

        # Normalize tất cả vector embedding
        faiss.normalize_L2(embeddings)

        # Tạo FAISS index với Inner Product cho cosine similarity
        self.faiss_index = faiss.IndexFlatIP(embeddings.shape[1])  # Inner Product (IP)
        self.faiss_index.add(embeddings)

        # Lưu ánh xạ giữa FAISS index và face_id
        self.face_id_map = {i: item["face_id"] for i, item in enumerate(db_embeddings)}
    
    """ ==================== detect faces ==================== """    
    def detect_faces(self, image_path):
        """
        Phát hiện khuôn mặt trong ảnh và trả về danh sách bounding box.
        """
        # Tải ảnh từ đường dẫn
        img = cv2.imread(image_path)

        # Sử dụng DeepFace để phát hiện khuôn mặt
        faces = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend=self.detector,
            enforce_detection = False,  # Không yêu cầu phát hiện khuôn mặt nếu ảnh đã chứa khuôn mặt
            align = True
        )

        # Kiểm tra nếu không phát hiện khuôn mặt
        if not faces:
            return {"message": "No faces detected"}, 400

        # Tạo danh sách bounding box từ kết quả phát hiện
        bounding_boxes = []
        for face in faces:
            box = face["facial_area"]  # Lấy tọa độ bounding box
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
        So sánh 2 ảnh và trả về độ giống nhau giữa chúng.
        """
        # Sử dụng DeepFace để so sánh 2 ảnh
        try:
            result = DeepFace.verify(
                image1_path,
                image2_path,
                model_name='SFace',
                detector_backend=self.detector,
                # metric: cosine, euclidean, euclidean_l2
                distance_metric='cosine',
                enforce_detection=True # Yêu cầu phát hiện khuôn mặt trước khi so sánh
            )

            # Trả về kết quả so sánh
            return {
                "verified": result["verified"],
                "distance": result["distance"],
                'threshold': result['threshold'],
            }
        except Exception as e:
            # Trả về lỗi nếu có vấn đề trong quá trình so sánh
            return {"error": str(e)}, 400
        
    """ ==================== liveness detection ==================== """
    def liveness_detection(self, image_path):
        """
        Kiểm tra liveness và chống giả mạo (anti-spoofing) từ ảnh đầu vào.
        """
        try:
            # Kiểm tra ảnh có hợp lệ không
            img = cv2.imread(image_path)
            
            
            if img is None:
                raise ValueError("Image could not be loaded. Check the file path.")

            # Gọi hàm extract_faces để phân tích khuôn mặt
            faces = DeepFace.extract_faces(
                img_path=image_path,
                detector_backend=self.detector,  # Bộ phát hiện khuôn mặt (opencv, mtcnn, ...)
                enforce_detection=True,          # Bắt buộc phát hiện khuôn mặt
                anti_spoofing=True               # Kích hoạt kiểm tra chống giả mạo
            )

            # Nếu không phát hiện khuôn mặt
            if not faces:
                return {"message": "No faces detected", "liveness": False, "spoofing": None}, 400

            # Duyệt qua các khuôn mặt được phát hiện
            results = []
            for face in faces:
                is_real = face.get("is_real", None)  # Trạng thái chống giả mạo
                spoof_score = face.get("antispoof_score", None)  # Điểm số chống giả mạo
                confidence = face.get("confidence", None)  # Độ tin cậy phát hiện khuôn mặt

                # Nếu kết quả hợp lệ, trả về trạng thái
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
        Truy xuất embeddings từ cơ sở dữ liệu PostgreSQL.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT face_id, user_id, embedding FROM Faces;")
            data = cursor.fetchall()

            # Chuyển đổi embedding JSON sang numpy array
            embeddings = [
                {
                    "face_id": row[0],
                    "user_id": row[1],
                    "embedding": np.array(row[2])  # Embedding dạng numpy array
                }
                for row in data
            ]
            return embeddings
        finally:
            cursor.close()
            conn.close()

    def extract_embedding(self, image_path):
        """
        Tạo embedding từ ảnh đầu vào bằng cách sử dụng DeepFace.
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
        Tìm kiếm khuôn mặt trong cơ sở dữ liệu bằng FAISS.
        """
        try:
            # Tạo embedding cho ảnh truy vấn
            query_embedding = self.extract_embedding(image_path)
            if query_embedding is None:
                return {"matched": False, "message": "No face detected in the image"}

            if self.faiss_index is None:
                self.build_faiss_index()

            # Normalize query embedding
            query_embedding = np.expand_dims(query_embedding, axis=0).astype('float32')
            faiss.normalize_L2(query_embedding)

            # Tìm kiếm nearest neighbor
            distances, indices = self.faiss_index.search(query_embedding, k=1)

            # Lấy kết quả tốt nhất
            best_index = indices[0][0]
            similarity = float(distances[0][0])  # Chuyển numpy.float32 sang float
            best_face_id = self.face_id_map[best_index]

            # Truy xuất thông tin khuôn mặt từ cơ sở dữ liệu
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
                    "similarity": similarity,  # Đã chuyển sang kiểu float
                    "user_id": user_id,
                    "image_base64": encoded_image
                }
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            return {"matched": False, "message": str(e)}