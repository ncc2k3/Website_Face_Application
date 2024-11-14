# repository/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get the current directory of the repository
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# directory of this project
ROOT_DIR = os.path.join(BASE_DIR, '..')

# Define the path to the data directory
DATA_DIR = os.path.join(ROOT_DIR, os.getenv('DATA'))
INPUT_DIR = os.path.join(DATA_DIR, os.getenv('INPUT'))
OUTPUT_DIR = os.path.join(DATA_DIR, os.getenv('OUTPUT'))

IDIR_IMGS = os.path.join(INPUT_DIR, os.getenv('IMAGE'))
IDIR_FS = os.path.join(INPUT_DIR, os.getenv('FACE_SEARCH'))
IDIR_FC = os.path.join(INPUT_DIR, os.getenv('FACE_COMPARISON'))

ODIR_FS = os.path.join(OUTPUT_DIR, os.getenv('FACE_SEARCH'))
ODIR_FC = os.path.join(OUTPUT_DIR, os.getenv('FACE_COMPARISON'))
ODIR_FD = os.path.join(OUTPUT_DIR, os.getenv('FACE_DETECTION'))
ODIR_LIVENESS = os.path.join(OUTPUT_DIR, os.getenv('LIVENESS'))

# Define metadata file paths
METADATA_FS = os.path.join(ODIR_FS, os.getenv('METADATA'))
METADATA_FC = os.path.join(ODIR_FC, os.getenv('METADATA'))
METADATA_FD = os.path.join(ODIR_FD, os.getenv('METADATA'))
METADATA_LIVENESS = os.path.join(ODIR_LIVENESS, os.getenv('METADATA'))


# path to popular dataset
RAW_DATASET = os.path.join(ROOT_DIR, os.getenv('RAW_DATASET'))

FDDB = os.path.join(ROOT_DIR, os.getenv('RAW_DATASET'), 'fddb', 'originalPics')
LFW = os.path.join(ROOT_DIR, os.getenv('RAW_DATASET'), 'lfw')
WIDER = os.path.join(ROOT_DIR, os.getenv('RAW_DATASET'), 'wider')
WIDER_VAL = os.path.join(WIDER, 'WIDER_val')


MESSI = os.path.join(IDIR_IMGS,'messi-face')


# # path of processed images
# OUT_FDDB = os.path.join(ODIR_FD, os.getenv('RAW_DATASET'), 'fddb', 'originalPics')
# OUT_LWF = os.path.join(ODIR_FD, os.getenv('RAW_DATASET'), 'lfw')
# OUT_WIDER = os.path.join(ODIR_FD, os.getenv('RAW_DATASET'), 'wider')
# OUT_WIDER_VAL = os.path.join(OUT_WIDER,'WIDER_val')


# if __name__ == "__main__":
#     print("Root Directory:", ROOT_DIR)
#     print("Data Directory:", DATA_DIR)
#     print("Input Directory:", INPUT_DIR)
#     print("Output Directory:", OUTPUT_DIR)
#     print("Images Input Directory:", IDIR_IMGS)
#     print("Face Search Input Directory:", IDIR_FS)
#     print("Face Comparison Input Directory:", IDIR_FC)
#     print("Face Detection Output Directory:", ODIR_FD)
#     print("Face Search Output Directory:", ODIR_FS)
#     print("Face Comparison Output Directory:", ODIR_FC)
#     print("Liveness Output Directory:", ODIR_LIVENESS)
#     print("Face Detection Metadata Path:", METADATA_FD)
#     print("Face Search Metadata Path:", METADATA_FS)
#     print("Face Comparison Metadata Path:", METADATA_FC)
#     print("Liveness Metadata Path:", METADATA_LIVENESS)
#     print("FDDB Dataset Path:", FDDB)
#     print("LFW Dataset Path:", LWF)
#     print("WIDER Dataset Path:", WIDER)
#     print("Processed FDDB Path:", OUT_FDDB)
#     print("Processed LFW Path:", OUT_LWF)
#     print("Processed WIDER Path:", OUT_WIDER)
#     print("WIDER Val Path:", WIDER_VAL)