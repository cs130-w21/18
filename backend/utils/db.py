import psycopg2
from psycopg2.extras import Json
import os

class DB:
    def __init__(self):
        self._conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    def initialize(self):
        create_moods = (
                "CREATE TABLE IF NOT EXISTS Moods ("
                "mood_id serial,"
                "name varchar,"
                "creator_id varchar,"
                "params json,"
                "PRIMARY KEY (name, creator_id)"
                ");"
                )
        self._cursor.execute(create_moods)
        #TODO: Create Users and Playlists tables

    def create_mood(self, name, creator_id, params):
        insert = (
                "INSERT INTO Moods("
                "name, creator_id, params"
                ") values (%s, %s, %s) RETURNING mood_id;" 
                )
        params = Json(params)
        self._cursor.execute(insert, (name, creator_id, params)) 
        return self._cursor.fetchone()[0]

    def update_mood(self, name, creator_id, params):
        update = (
                "UPDATE Moods SET params = %s "
                "WHERE name = %s AND creator_id = %s RETURNING mood_id;"
                )
        self._cursor.execute(update, (params, name, creator_id))
        return self._cursor.fetchone()[0]

    def get_mood_by_name(self, name, creator_id):
        select = (
                "SELECT * FROM Moods WHERE name = %s AND creator_id = %s;"
                )
        self._cursor.execute(select, (name, creator_id))
        row = self._cursor.fetchone()
        if row is None:
            return None, None
        return row[0], row[3]

    def get_mood_by_id(self, mood_id):
        select = (
                "SELECT * FROM Moods WHERE mood_id = %s;"
                )
        self._cursor.execute(select, (mood_id))
        row = self._cursor.fetchone()
        if row is None:
            return None, None, None
        return row[1], row[2], row[3]

    def delete_mood(self, name, creator_id):
        delete = (
                "DELETE FROM Moods WHERE name = %s AND creator_id = %s RETURNING *;"
                )
        self._cursor.execute(delete, (name, creator_id))
        row = self._cursor.fetchone()
        if row is None:
            return None, None
        return row[0], row[3]
