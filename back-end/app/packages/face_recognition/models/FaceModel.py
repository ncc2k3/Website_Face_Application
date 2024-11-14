from app.config.Database import facedb
from sqlalchemy.dialects.postgresql import ARRAY
import numpy as np
import json


class Face(facedb.Model):

    __tablename__ = 'face'
    
    id = facedb.Column(facedb.Integer, primary_key=True)
    # name = facedb.Column(facedb.String(50), nullable=False)
    embedding = facedb.Column(facedb.JSON, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    
    def __init__(self,id,embedding):
        self.id = id
        self.embedding = embedding

    def add_face(self,image):
        pass

    pass
