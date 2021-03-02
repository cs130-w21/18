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
        create_users = (
                "CREATE TABLE IF NOT EXISTS User ("
                "user_id varchar PRIMARY KEY,"
                "moods integer[] DEFAULT array[]::integer[]"
                ");"
                )
        self._cursor.execute(create_moods)
        self._cursor.execute(create_users)
        #TODO: Create Users and Playlists tables

    def create_mood(self, name, creator_id, params):
        insert = (
                "INSERT INTO Moods("
                "name, creator_id, params"
                ") values (%s, %s, %s) RETURNING mood_id;" 
                )
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
        self._cursor.execute(select, (mood_id,))
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

    def create_user(self, user_id):
        insert = (
                "INSERT INTO Users (user_id) values (%s);"
                )
        try:
            self._cursor.execute(insert, (user_id,))
        except psycopg2.Error as e:
            return False
        return True

    def get_user_mood_ids(self, user_id):
        select = (
                "SELECT * FROM Users WHERE user_id = %s;"
                )
        self._cursor.execute(select, (user_id,))
        row = self._cursor.fetchone()
        if row is None:
            return None
        return row[1]

    def get_user_moods(self, user_id):
        moods = self.get_user_mood_ids(user_id)
        if moods is None:
            return None
        select = (
                "SELECT mood_id, name, params FROM Moods WHERE mood_id = ANY(%s);"
                )
        self.cursor.execute(select, (moods,))
        rows = self._cursor.fetch
        if rows is None:
            return None
        return [{'mood_id': row[0], 'mood_name': row[1], **row[2]} for row in rows]

    def add_mood_for_user(self, user_id, mood_id):
        user_moods = self.get_user_mood_ids(user_id)
        if user_moods is None:
            return False
        if mood_id in user_moods:
            return False
        update = (
                "UPDATE Users SET moods = array_append(moods, %s) "
                "WHERE user_id = %s;"
                )
        try:
            self.cursor.execute(update, (mood_id, user_id))
        except psycopg2.Error as e:
            return False
        return True
