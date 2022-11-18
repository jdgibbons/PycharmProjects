import psycopg2
from config import config


def get_parts(vendor_id):
    conn = None

    try:
        params = config()

        conn = psycopg2.connect(**params)

        curse = conn.cursor()

        curse.callproc('get_parts_by_vendor', (vendor_id,))

        row = curse.fetchone()

        while row is not None:
            print(row)
            row = curse.fetchone()

        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


get_parts(8)
