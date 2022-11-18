import psycopg2
from config import config


def write_blob(part_id, path_to_file, file_extension):
    """ INSERT a BLOB into a table """
    conn = None

    try:
        drawing = open(path_to_file, 'rb').read()

        params = config()

        conn = psycopg2.connect(**params)

        curse = conn.cursor()

        curse.execute("INSERT INTO part_drawings(part_id, file_extension, drawing_data) " +
                      "VALUES(%s, %s, %s)",
                      (part_id, file_extension, psycopg2.Binary(drawing)))

        conn.commit()
        curse.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


write_blob(1, 'images/simtray.jpg.old', 'jpg')
write_blob(2, 'images/speaker.jpg.old', 'jpg')
