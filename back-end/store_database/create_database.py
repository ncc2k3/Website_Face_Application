import os
import psycopg2
from flask_bcrypt import Bcrypt
from faker import Faker
from deepface import DeepFace
import json

# Configure PostgreSQL connection
db_config = {
    'dbname': 'cv_project',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Path to the folder containing images
image_folder = os.path.join(os.getcwd(), 'store_database', 'imgs_database_faces')

# Create Flask-Bcrypt and Faker objects
bcrypt = Bcrypt()
faker = Faker()

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to PostgreSQL successfully!")
except Exception as e:
    print(f"Connection error: {e}")
    exit()

# Get current link
# Get list of images from folder
def get_images_from_folder(folder_path):
    """Get list of image files in a folder."""
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Create hashed password
def hash_password(password):
    """Hash password using flask-bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Add user to Users table
def add_user(first_name, last_name, email, password):
    """Add a user to the Users table."""
    cursor.execute("""
    INSERT INTO Users (first_name, last_name, email, password)
    VALUES (%s, %s, %s, %s) RETURNING user_id;
    """, (first_name, last_name, email, password))
    conn.commit()
    return cursor.fetchone()[0]

# Add face to Faces table
def add_face(user_id, image_name, image_path, embedding):
    """Add a face to the Faces table."""
    cursor.execute("""
    INSERT INTO Faces (user_id, image_name, image_path, embedding)
    VALUES (%s, %s, %s, %s);
    """, (user_id, image_name, image_path, json.dumps(embedding)))
    conn.commit()

# Create data from images
def create_data_from_images(folder_path):
    """Create data from images and add to the database."""
    image_paths = get_images_from_folder(folder_path)
    for image_path in image_paths:
        try:
            # Generate random user information
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            password = hash_password("123")

            # Add user to table
            user_id = add_user(first_name, last_name, email, password)

            # Process embedding from image
            image_name = os.path.basename(image_path)
            embedding = DeepFace.represent(img_path=image_path, model_name="SFace")[0]["embedding"]

            # Add face to Faces table
            add_face(user_id, image_name, image_path, embedding)
            print(f"Successfully added: {image_name} -> User ID: {user_id}")

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

# Execute steps
try:
    create_data_from_images(image_folder)
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
    print("Disconnected from PostgreSQL.")
