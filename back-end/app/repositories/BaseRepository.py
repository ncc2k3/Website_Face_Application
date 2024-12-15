from app.config.Database import get_connection

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def find_by_user_id(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {self.model.__tablename__} WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                record = cursor.fetchone()
                if record:
                    return self.model(*record)
                return None
