import os
from deepface import DeepFace
import psycopg2
import logging
import pandas as pd

# Disable truncation
pd.set_option("display.max_rows", None)  # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", None)  # Prevent wrapping of lines
pd.set_option("display.max_colwidth", None)  # Show full content in each column

# Logging configuration
logging.basicConfig(level=logging.INFO)


def get_embedding(image_path, model_name="SFace", detector_backend="opencv"):
    """Extracts face embedding using DeepFace."""
    try:
        try:
            img_objs = DeepFace.extract_faces(
                img_path=image_path,
                detector_backend=detector_backend,
                align=True,
                grayscale=False,
            )
        except ValueError as e:
            logging.error(f"Failed to extract faces for {image_path}: {e}")
            img_objs = []

        if len(img_objs) != 0:
            # for img_obj in img_objs:
            img_content = img_objs[0]["face"]
            embedding = DeepFace.represent(
                img_content, model_name=model_name, detector_backend="skip"
            )[0]["embedding"]
            return embedding

        else:
            return None

    except Exception as e:
        logging.error(f"Failed to get embedding for {image_path}: {e}")
        return None


def get_embeddings(image_dir):
    """Collects embeddings for all images in the given directory."""
    representations = []
    for dirpath, dirnames, filenames in os.walk(image_dir):
        for filename in filenames:
            if filename.endswith(".jpg"):
                image_path = os.path.join(dirpath, filename).replace("\\", "/")
                embedding = get_embedding(image_path)
                if embedding:
                    representations.append((image_path, embedding))
    return representations


def create_table(cur):
    """Creates embeddings table."""
    cur.execute(
        "CREATE TABLE IF NOT EXISTS embeddings (name VARCHAR, embedding DECIMAL[]);"
    )


def drop_table(cur, table_name="embeddings"):
    """Drops table if exists."""
    cur.execute(f"DROP TABLE IF EXISTS {table_name};")


def insert_data(cur, representations):
    """Inserts data into the embeddings table."""
    for img_path, embedding in representations:
        cur.execute(
            f"INSERT INTO embeddings (name, embedding) VALUES ('{img_path}', ARRAY{embedding});"
        )


def query(cur, target_emb, target_img):
    """Queries the database for similar embeddings."""
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
        WHERE distance < 10.734
        ORDER BY distance;
    """
    )
    return cur.fetchall()


def face_search(target_path, cur):
    """Performs face search for the given image."""
    target_emb = get_embedding(target_path)
    if not target_emb:
        logging.error("Failed to extract embedding for target image.")
        return []
    return query(cur, target_emb, target_path)


if __name__ == "__main__":
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fs",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "123"),
            port="5432",
        )
        cur = conn.cursor()

        # # Drop and recreate table
        # drop_table(cur)
        # create_table(cur)

        # # Collect and insert embeddings
        # image_dir = "C:/Users/Admin/Documents/CV/deepface/tests/dataset"
        # representations = get_embeddings(image_dir)
        # if representations:
        #     insert_data(cur, representations)
        #     conn.commit()
        #     logging.info("Embeddings inserted successfully.")

        # Perform face search
        target_img = "C:/Users/Admin/Documents/CV/deepface/tests/dataset/img1.jpg"
        if os.path.exists(target_img):
            results = face_search(target_img, cur)
            for item in results:
                print(item)
        else:
            logging.error(f"Target image {target_img} does not exist.")

    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()


# target_path = "C:/Users/Admin/Documents/CV/deepface/tests/dataset/img1.jpg" 
# # "C:/Users/Admin/Documents/CV/face-recognition-app/data/input/imgs/messi-face/Image_2.jpg"
# img_dir = "C:/Users/Admin/Documents/CV/deepface/tests/dataset/"
# # "C:/Users/Admin/Documents/CV/face-recognition-app/data/input/imgs/messi-face"

# finds = DeepFace.find(
#     img_path=target_path,
#     db_path=img_dir,
#     model_name="SFace",
#     detector_backend="opencv",
#     distance_metric="euclidean",
#     anti_spoofing=True,
# )

# for item in finds:
#     print(item["identity"], item["distance"], item["threshold"])
