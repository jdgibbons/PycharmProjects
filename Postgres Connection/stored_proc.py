import psycopg2
from config import config


def add_part(part_name, vendor_name):
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        curse = conn.cursor()

        curse.execute('CALL add_new_part(%s, %s)', (part_name, vendor_name))

        conn.commit()

        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


add_part('OLED', 'LG')
