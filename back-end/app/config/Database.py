import psycopg2
from psycopg2 import sql
from app.config.AppConfig import Config

# Thông tin kết nối
DATABASE_CONFIGURATION = {
    'dbname': Config.DATABASE_CONFIG['dbname'],
    'user': Config.DATABASE_CONFIG['user'],
    'password': Config.DATABASE_CONFIG['password'],
    'host': Config.DATABASE_CONFIG['host'],
    'port': Config.DATABASE_CONFIG['port']
}

# Tạo kết nối và con trỏ
def get_connection():
    print(DATABASE_CONFIGURATION.get('dbname'))
    conn = psycopg2.connect(**DATABASE_CONFIGURATION)
    return conn