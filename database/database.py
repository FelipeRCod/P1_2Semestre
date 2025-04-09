from contextlib import contextmanager
import mysql.connector
import os

@contextmanager
def get_connection(database=None):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWD"),
            database=database
        )
        yield conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()

@contextmanager
def get_cursor(database=None):
    with get_connection(database) as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()