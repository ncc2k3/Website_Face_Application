import cv2
from deepface import DeepFace
from app.config.Database import get_connection
from scipy.spatial.distance import cosine
import numpy as np
import base64
import os

class FaceRecognitionService:
    def __init__(self):
        self.detector = 'opencv'  # Sử dụng YuNet làm detector trong DeepFace
        self.model = 'SFace'  # Sử dụng SFace model trong DeepFace
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
                # distance_metric='euclidean_l2',
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
                    "embedding": np.array(row[2])  # Chuyển đổi embedding JSON sang numpy array
                }
                for row in data
            ]
            return embeddings
        finally:
            cursor.close()
            conn.close()

    def calculate_similarity(self, query_embedding, db_embeddings):
        """
        Tính toán độ tương đồng giữa query_embedding và tất cả embeddings trong database.
        """
        results = []
        for item in db_embeddings:
            similarity = 1 - cosine(query_embedding, item["embedding"])  # Sử dụng cosine similarity
            results.append({
                "face_id": item["face_id"],
                "user_id": item["user_id"],
                "similarity": similarity
            })
        # Sắp xếp theo độ tương đồng giảm dần
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)
        return results

    def extract_embedding(self, image_path):
        """
        Tạo embedding từ ảnh đầu vào bằng cách sử dụng DeepFace.
        """
        try:
            # Sử dụng DeepFace để tạo embedding
            embeddings = DeepFace.represent(
                img_path=image_path,
                model_name=self.model,  # Model SFace
                detector_backend=self.detector,  # Bộ phát hiện khuôn mặt
                enforce_detection=True  # Bắt buộc phát hiện khuôn mặt
            )
            
            # Kiểm tra nếu không có embedding được tạo
            if not embeddings:
                return None

            # Trả về embedding đầu tiên (thường ảnh chỉ có một khuôn mặt)
            return embeddings[0]["embedding"]

        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def search_face(self, image_path):
        try:
            query_embedding = self.extract_embedding(image_path)
            if query_embedding is None:
                return {"matched": False, "message": "No face detected in the image"}

            db_embeddings = self.get_embeddings_from_db()
            results = self.calculate_similarity(query_embedding, db_embeddings)
            # print(results)
            if results and len(results) > 0:
                best_match = results[0]
                conn = get_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT image_path FROM Faces WHERE face_id = %s;", (best_match["face_id"],))
                    image_path_db = cursor.fetchone()[0]
                    # print("-----------------")
                    # print(f"Best match found: {best_match['user_id']} with similarity {best_match['similarity']}")
                    # print(f"Image path: {image_path_db}")
                    if not os.path.exists(image_path_db):
                        return {"matched": False, "message": "Image file does not exist in database"}

                    with open(image_path_db, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

                    return {
                        "matched": True,
                        "similarity": best_match["similarity"],
                        "user_id": best_match["user_id"],
                        "image_base64": encoded_image
                    }
                finally:
                    cursor.close()
                    conn.close()
            else:
                return {"matched": False, "message": "No match found"}

        except Exception as e:
            return {"matched": False, "message": str(e)}

