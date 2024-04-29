import psycopg2

from .db_config import host, user, password, db_name


def db_info():
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM mgdle_data'
            )
            return cursor.fetchall()

    except Exception as ex:
        print("[INFO] Error while working with DB", ex)
        return 'Error'



