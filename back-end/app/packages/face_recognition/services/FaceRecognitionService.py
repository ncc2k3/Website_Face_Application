import cv2
from deepface import DeepFace

class FaceRecognitionService:
    def __init__(self):
        self.detector = 'yunet'  # Sử dụng YuNet làm detector trong DeepFace

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
            return {"message": "No faces detected"}, 200

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
        result = DeepFace.verify(
            image1_path=image1_path,
            image2_path=image2_path,
            model_name='Facenet',
            detector_backend=self.detector
        )

        # Trả về kết quả so sánh
        return {
            "verified": result["verified"],
            "distance": result["distance"]
        }