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
                "CREATE TABLE IF NOT EXISTS Users ("
                "user_id varchar PRIMARY KEY,"
                "created_moods integer[] DEFAULT array[]::integer[],"
                "external_moods integer[] DEFAULT array[]::integer[],"
                "refresh_token varchar"
                ");"
                )
        create_playlists = (
                "CREATE TABLE IF NOT EXISTS Playlists ("
                "creator_id varchar,"
                "mood_id integer,"
                "idx integer,"
                "uri varchar UNIQUE NOT NULL,"
                "PRIMARY KEY (creator_id, mood_id, idx)"
                ");"
                )
        self._cursor.execute(create_moods)
        self._cursor.execute(create_users)
        self._cursor.execute(create_playlists)

    def create_mood(self, name, creator_id, params):
        insert = (
                "INSERT INTO Moods("
                "name, creator_id, params"
                ") values (%s, %s, %s) RETURNING mood_id;" 
                )
        self._cursor.execute(insert, (name, creator_id, params)) 
        mood_id = self._cursor.fetchone()[0]
        self.add_mood_for_user(creator_id, mood_id, is_external=False)
        return mood_id

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

    def create_or_update_user(self, user_id, refresh_token):
        insert_or_update = None
        if self._user_exists(user_id):
            insert_or_update = (
                    "UPDATE Users SET refresh_token = %s WHERE user_id = %s;"
                    )
        else:
            insert_or_update = (
                    "INSERT INTO Users (refresh_token, user_id) values (%s, %s);"
                    )
        try:
            self._cursor.execute(insert_or_update, (refresh_token, user_id))
        except psycopg2.Error as e:
            return False
        return True

    def get_user_moods(self, user_id):
        created_moods, external_moods = self._get_user_mood_ids(user_id)
        if created_moods is None:
            return None
        created_mood_rows = self._get_mood_rows(created_moods)
        external_mood_rows = self._get_mood_rows(external_moods)
        if created_mood_rows is None or external_mood_rows is None:
            return None

        return {
                'created_moods': self._convert_mood_rows_to_list(created_mood_rows),
                'external_moods': self._convert_mood_rows_to_list(external_mood_rows)
                }

    def add_mood_for_user(self, user_id, mood_id, is_external):
        created_moods, external_moods = self._get_user_mood_ids(user_id)
        if created_moods is None:
            return False
        if mood_id in created_moods or mood_id in external_moods:
            return False
        if is_external:
            update = (
                    "UPDATE Users SET external_moods = array_append(external_moods, %s) "
                    "WHERE user_id = %s;"
                    )
        else:
            update = (
                    "UPDATE Users SET created_moods = array_append(created_moods, %s) "
                    "WHERE user_id = %s;"
                    )
        try:
            self._cursor.execute(update, (mood_id, user_id))
        except psycopg2.Error as e:
            return False
        return True

    def get_recent_moods(self, user_id):
        recent_moods = []
        other_users = []
        other_user_ids = self._get_other_user_ids(user_id)
        for other_user in other_user_ids:
            created_moods, _ = self._get_user_mood_ids(other_user[0])
            if created_moods is None:
                continue
            recent_moods.append(self._get_mood_rows(created_moods)[-1])  # get most recent mood row
            other_users.append(other_user[0])
        return self._convert_mood_rows_to_list(recent_moods), other_users

    def create_playlist_on_mood(self, creator_id, mood_id, uri):
        idx = self.get_next_playlist_idx_for_mood(creator_id, mood_id)
        if idx is None:
            return None
        insert = (
                "INSERT INTO Playlists("
                "creator_id, mood_id, idx, uri"
                ") values (%s, %s, %s, %s);"
                )
        try:
            self._cursor.execute(insert, (creator_id, mood_id, idx, uri))
        except psycopg2.Error:
            return None
        return idx

    def get_mood_playlists(self, creator_id, mood_id):
        select = (
                "SELECT * FROM Playlists WHERE "
                "creator_id = %s AND mood_id = %s;"
                )
        self._cursor.execute(select, (creator_id, mood_id))
        rows = self._cursor.fetchall()
        return rows

    def get_next_playlist_idx_for_mood(self, creator_id, mood_id):
        select_playlist_count = (
                "SELECT COALESCE(max(idx), 0) FROM Playlists WHERE "
                "creator_id = %s AND mood_id = %s;"
                )
        self._cursor.execute(select_playlist_count, (creator_id, mood_id))
        row = self._cursor.fetchone()
        if row is None:
            return None
        return row[0] + 1

    def _user_exists(self, user_id):
        row = self._get_user_row(user_id)
        if row is None:
            return False
        return True

    def _get_user_mood_ids(self, user_id):
        row = self._get_user_row(user_id)
        if row is None:
            return None, None
        return row[1], row[2]

    def _get_user_row(self, user_id):
        select = (
                "SELECT * FROM Users WHERE user_id = %s;"
                )
        self._cursor.execute(select, (user_id,))
        row = self._cursor.fetchone()
        return row

    def _get_mood_rows(self, mood_ids):
        select = (
                "SELECT * FROM Moods WHERE mood_id = ANY(%s);"
                )
        self._cursor.execute(select, (mood_ids,))
        return self._cursor.fetchall()

    def _convert_mood_rows_to_list(self, mood_rows):
        return [{'mood_id': row[0], 'mood_name': row[1], 'params': row[3]} for row in mood_rows]

    def _get_other_user_ids(self, user_id):
        select = (
                "SELECT user_id FROM Users WHERE user_id != %s;"
                )
        self._cursor.execute(select, (user_id,))
        return self._cursor.fetchall()
