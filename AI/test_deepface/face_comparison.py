import gc
from deepface import DeepFace
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Paths to two images for comparison
img1_path = r"C:\Users\HuyTP\Documents\CV\face-recognition-app\data\input\imgs\messi-face\Image_1.jpg"
img2_path = r"C:\Users\HuyTP\Documents\CV\face-recognition-app\data\input\imgs\alok-face\Image_2.jpg"

# Choose yunet: lightweight and highly accurate
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

# Choose euclidean_l2
metrics = [
    # 'cosine',
    # 'euclidean',
    'euclidean_l2'
]

# Choose SFace because of stable accuracy and medium size
models = [
    # 'Facenet512',
    # 'Facenet',
    # 'VGG-Face',
    # 'Dlib',
    # 'ArcFace',
    # 'GhostFaceNet',
    # 'OpenFace',
    # 'DeepFace',
    # 'DeepID',
    'SFace',
]

# Not necessary
normalizaton = [
    'base',
    'raw',
    'Facenet',
    'Facenet2018',
    'VGGFace',
    'VGGFace2',
    'ArcFace'
]

# Initialize a list to store results for printing
results = []

for model_name in models:
    print(f'\n{model_name}')
    for metric in metrics:
        print(f'\n{metric}')
        for detector in detectors:
            print(f'\n{detector}')
            # Compare faces
            result = DeepFace.verify(img1_path,
                                     img2_path,
                                     model_name=model_name,
                                     distance_metric=metric,
                                     detector_backend=detector,
                                     enforce_detection=False)
            # Store result
            results.append(result)
            
    print('='*10)


# Print summary table header
print("\n" + "=" * 70)
print(f"| {'Model':<20} | {'Distance':<10} | {'Detector':<15} | {'Threshold':<10} | {'Distance Metric':<15} | {'Time (s)':<10} | {'Verified':<10} |")
print("=" * 70)

# Print each result in the summary table
for result in results:
    print(f"| {result['model']:<20} | {result['distance']:<10.4f} | {result['detector_backend']:<15} | {result['threshold']:<10.4f} | {result['similarity_metric']:<15} | {result['time']:<10.4f} | {str(result['verified']):<10} |")
