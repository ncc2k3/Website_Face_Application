import cv2
from deepface import DeepFace

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

    def face_search(self, image_path,threshold=10.734):
        """
        Tiìm kiếm khuôn mặt trong ảnh và trả về danh sách khuôn mặt phân tích.
        """
        # Sử dụng DeepFace để tiìm kiếm khuôn mặt trong ảnh

        target_emb = self.get_face_embedding(image_path)
        if not target_emb:
            return []

        # Trả về danh sách khuôn mặt phân tích
        results = self.query(target_emb,threshold)

        if len(results) == 0:
            return []
        
        return results[0]

    def get_face_embedding(self, image_path):
        """
        Lấy embedding ảnh khuôn mặt.
        """
        # Sử dụng DeepFace để lấy embedding ảnh khuôn mặt

        try:
            try:
                img_objs = DeepFace.extract_faces(
                    img_path=image_path,
                    detector_backend=self.detector,
                    align=True,
                    grayscale=False,
                )
            except ValueError as e:
                # logging.error(f"Failed to extract faces for {image_path}: {e}")
                img_objs = []

            if len(img_objs) != 0:
                img_content = img_objs[0]["face"]
                embedding = DeepFace.represent(
                    img_content, model_name=self.model, detector_backend="skip"
                )[0]["embedding"]
                return embedding

            else:
                return None
            
        except Exception as e:
            # logging.error(f"Failed to get embedding for {image_path}: {e}")
            return None
        
    def query(self, cur, target_emb, threshold):

        """Queries the database "faces" for similar embeddings."""
        cur.execute(
            f"""
            SELECT * FROM (
                SELECT name, SQRT(SUM(distance)) AS distance
                    FROM (
                        SELECT name, POW(UNNEST(embedding) - UNNEST(ARRAY{target_emb}), 2) AS distance
                        FROM embeddings
                    ) sq1
                GROUP BY name
            ) sq2
            WHERE distance < {threshold}
            ORDER BY distance;
        """
        )
        return cur.fetchall()
    
    def insert_data(self, cur,img_data):
        try:
            img = cv2.imread(img_data)
            emb = self.get_face_embedding(img)
            cur.execute(
                f"INSERT INTO embeddings (name, embedding) VALUES ('{img}', ARRAY{emb});"
            )
        except Exception as e:
            # logging.error(f"Failed to insert data: {e}")
            return None
