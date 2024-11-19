from app.config.Database import get_connection

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def find_by_id(self, id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {self.model.__tablename__} WHERE id = %s"
                cursor.execute(query, (id,))
                record = cursor.fetchone()
                if record:
                    return self.model(*record)
                return None
