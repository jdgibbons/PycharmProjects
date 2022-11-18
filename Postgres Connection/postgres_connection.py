import psycopg2
from config import config


def connect():
    conn = None

    try:
        params = config()

        print('Connecting to the PostgreSQL database . . .')
        print('Params:')
        for key in params.keys():
            print(f"{key} = {params[key]}")

        conn = psycopg2.connect(**params)

        curse = conn.cursor()
        curse.execute('SELECT version()')

        db_version = curse.fetchone()

        print(f"PostgreSQL database version: {db_version}")

        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


connect()