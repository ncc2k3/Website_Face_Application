import psycopg2
from psycopg2 import sql

# Thông tin kết nối
DATABASE_CONFIG = {
    'dbname': 'cv_project',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Tạo kết nối và con trỏ
def get_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn