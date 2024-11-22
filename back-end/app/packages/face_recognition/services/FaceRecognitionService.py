import cv2
from deepface import DeepFace

class FaceRecognitionService:
    def __init__(self):
        self.detector = 'opencv'  # Sử dụng YuNet làm detector trong DeepFace

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
                align=True,                      # Căn chỉnh khuôn mặt
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
                    "spoofing_score": spoof_score
                })

            return {"message": "Liveness detection completed", "results": results}, 200

        except Exception as e:
            return {"error": str(e)}, 400
