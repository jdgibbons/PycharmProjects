import psycopg2
from config import config


def get_vendors():
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        curse = conn.cursor()
        curse.execute(""" SELECT vendor_id, vendor_name
                          FROM vendors
                          ORDER BY vendor_name """)
        print(f"The number of vendors: {curse.rowcount}")

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


get_vendors()
