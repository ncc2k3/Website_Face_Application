from deepface import DeepFace
import matplotlib.pyplot as plt
import os
import time
import json
from repository.config import *

detectors = [
    # 'opencv',
    # 'retinaface',
    # 'mtcnn',
    # 'fastmtcnn',
    # 'ssd',
    # 'dlib',
    # 'mediapipe',
    # 'yolov8',
    # 'centerface',
    # 'skip',
    'yunet'
]

input_dataset = MESSI

# Define a tuple of image file extensions
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

# Walk through the directory tree from input_base_dir
for dirpath, dirnames, filenames in os.walk(input_dataset):
    
    # Calculate the relative path from the input_base_dir to the current dirpath
    relative_path = os.path.relpath(dirpath, start=input_dataset)

    # Define the corresponding directory path in the output directory for each image file
    for filename in filenames:
        
        # Remove the extension from the filename to use as the directory name
        image_name = os.path.splitext(filename)[0]
        
        # Define the full output directory path for this image
        image_output_dir = os.path.join(ODIR_FD, relative_path, image_name)
        
        # Create the output directory for the image
        os.makedirs(image_output_dir, exist_ok=True)

        img_path = os.path.join(dirpath, filename)
        
        for detector in detectors:
            output_dir = os.path.join(image_output_dir, detector)
            os.makedirs(output_dir, exist_ok=True)
            start_time = time.time()

            # Detect faces
            detected_faces = DeepFace.extract_faces(
                img_path=img_path,
                anti_spoofing=True,
                detector_backend=detector,
                enforce_detection=False
            )

            end_time = time.time()
            
            # Create a list to hold metadata for each detected face
            results = []
            for i, meta_face in enumerate(detected_faces):
                face_data = {
                    "face_index": i + 1,
                    "confidence_score": meta_face['confidence'],
                    "anti_spoof_score": meta_face['antispoof_score'],
                    "is_real": meta_face['is_real'],
                    "bounding_box": meta_face['facial_area'],
                    "detection_time": end_time - start_time,
                }
                
                # Add eye coordinates if they exist
                if 'left_eye' in meta_face['facial_area']:
                    face_data["left_eye"] = meta_face['facial_area']['left_eye']
                if 'right_eye' in meta_face['facial_area']:
                    face_data["right_eye"] = meta_face['facial_area']['right_eye']
                
                results.append(face_data)

                # Save each face image without annotations
                face = meta_face['face']
                fig, ax = plt.subplots()
                ax.imshow(face)
                ax.axis('off')
                
                # Save the face image
                output_face_path = os.path.join(output_dir, f"face_{i + 1}.png")
                plt.savefig(output_face_path, bbox_inches='tight', pad_inches=0.1)
                plt.close()

            # Save metadata to a JSON file
            json_path = os.path.join(output_dir, "results.json")
            with open(json_path, "w") as json_file:
                json.dump(results, json_file, indent=4)

print("DONE!!!")
