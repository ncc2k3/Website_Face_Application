from app import create_app
from flask import render_template
from app.config.AppConfig import Config
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

app = create_app()

if __name__ == '__main__':
    app.run(host="localhost", port=Config.PORT, debug=True)
