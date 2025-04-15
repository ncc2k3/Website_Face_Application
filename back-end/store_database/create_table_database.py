import psycopg2
from flask_bcrypt import Bcrypt

# Create Bcrypt object
bcrypt = Bcrypt()

# Configure PostgreSQL connection
db_config = {
    "dbname": "your_database_name",  # Replace database name
    "user": "your_username",         # Replace PostgreSQL username
    "password": "your_password",     # Replace PostgreSQL password
    "host": "localhost",             # Host
    "port": "5432"                   # PostgreSQL port (default: 5432)
}

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to PostgreSQL successfully!")
except Exception as e:
    print(f"Connection error: {e}")
    exit()

# Create Users table
try:
    cursor.execute("""
    DROP TABLE IF EXISTS Faces CASCADE;
    DROP TABLE IF EXISTS Users CASCADE;
    
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(256) NOT NULL,  # Store hashed password
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Users table created successfully!")
except Exception as e:
    print(f"Error creating Users table: {e}")

# Create Faces table
try:
    cursor.execute("""
    CREATE TABLE Faces (
        face_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
        image_name VARCHAR(255) NOT NULL,
        image_path VARCHAR(255) NOT NULL,
        embedding JSONB NOT NULL, # Store embeddings as JSON
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Faces table created successfully!")
except Exception as e:
    print(f"Error creating Faces table: {e}")

# Close connection
cursor.close()
conn.close()
print("Database setup completed.")
