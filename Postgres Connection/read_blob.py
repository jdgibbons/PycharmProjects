import psycopg2
from config import config


def read_blob(part_id, path_to_dir):
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        curse = conn.cursor()

        curse.execute(""" SELECT part_name, file_extension, drawing_data
                          FROM part_drawings
                          INNER JOIN parts on parts.part_id = part_drawings.part_id
                          WHERE parts.part_id = %s """,
                      (part_id,))

        blob = curse.fetchone()
        open(path_to_dir + blob[0] + '.' + blob[1], 'wb').write(blob[2])

        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


read_blob(2, 'images/')