import psycopg2
from config import config

def insert_vendor(vendor_name):
    sql = """
          INSERT INTO vendors(vendor_name)
          VALUES(%s) RETURNING vendor_id;
          """

    conn = None
    vendor_id = None

    try:
        params = config()
        conn = psycopg2.connect(**params)

        curse = conn.cursor()
        curse.execute(sql, (vendor_name,))
        vendor_id = curse.fetchone()[0]

        conn.commit()
        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


def insert_vendor_list(vendor_list):
    sql = "INSERT INTO vendors(vendor_name) VALUES (%s)"
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)

        curse = conn.cursor()
        curse.executemany(sql, vendor_list)

        conn.commit()

        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


insert_vendor("3M Co.")
# insert multiple vendors
insert_vendor_list([
    ('AKM Semiconductor Inc.',),
    ('Asahi Glass Co Ltd.',),
    ('Daikin Industries Ltd.',),
    ('Dynacast International Inc.',),
    ('Foster Electric Co. Ltd.',),
    ('Murata Manufacturing Co. Ltd.',)
])
