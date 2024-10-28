
from app.config.Database import userdb

class BaseRepository:
    def __init__(self, model, session):
        # print("Base repo")
        self.model = model
        self.session = session
    
    def add(self, instance):
        userdb.session.add(instance)
        userdb.session.commit()

    def update(self):
        userdb.session.commit()