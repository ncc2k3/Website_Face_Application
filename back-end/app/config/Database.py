# import mysql.connector

# connection = mysql.connector(
#     host = "localhost",
#     user = "root",
#     password = ""
# )

# cursor = connection.cursor()

# User Database
from flask_sqlalchemy import SQLAlchemy

userdb = SQLAlchemy()  # Khởi tạo SQLAlchemy mà không truyền vào app
