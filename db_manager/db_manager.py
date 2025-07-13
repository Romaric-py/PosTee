import sqlite3
from contextlib import contextmanager

class DBManager:
    def __init__(self, db_path="my_database.db"):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # important pour avoir Row objets (dict-like)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def get_cursor(self):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[ERREUR] Requête échouée : {e}")
            raise
        finally:
            conn.close()

    def execute(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid

    def execute_many(self, query, params_list):
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)

    def execute_script(self, script):
        with self.get_cursor() as cursor:
            cursor.executescript(script)

    def execute_sql_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            script = f.read()
        self.execute_script(script)

    def fetch_one(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()  # retourne sqlite3.Row ou None

    def fetch_all(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()  # liste de sqlite3.Row

    def fetch_all_with_description(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            data = cursor.fetchall()
            description = cursor.description
            return data, description
