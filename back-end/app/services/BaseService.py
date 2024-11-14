from app.repositories.BaseRepository import BaseRepository
class BaseService:
    def __init__(self, model):
        # print("Base Service")
        self.repository = BaseRepository(model)