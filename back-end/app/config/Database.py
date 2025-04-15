import psycopg2
from psycopg2 import sql
from app.config.AppConfig import Config

# Connection information
DATABASE_CONFIGURATION = {
    'dbname': Config.DATABASE_CONFIG['dbname'],
    'user': Config.DATABASE_CONFIG['user'],
    'password': Config.DATABASE_CONFIG['password'],
    'host': Config.DATABASE_CONFIG['host'],
    'port': Config.DATABASE_CONFIG['port']
}

# Create connection and cursor
def get_connection():
    print(DATABASE_CONFIGURATION.get('dbname'))
    conn = psycopg2.connect(**DATABASE_CONFIGURATION)
    return conn