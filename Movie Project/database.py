# title, release_date, watched
import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
                         title TEXT,
                         release_timestamp REAL
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
                          watcher_name TEXT,
                          title TEXT
)
"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
DELETE_MOVIES = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"
INSERT_WATCHED_MOVIES = "INSERT INTO watched (watcher_name, title) VALUES (?, ?);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 where title = ?;"


connection = sqlite3.connect('movies.db')


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)


def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        curse = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            curse.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            curse.execute(SELECT_ALL_MOVIES)
        return curse.fetchall()


def watch_movie(viewer, title):
    with connection:
        connection.execute(DELETE_MOVIES, (title,))
        connection.execute(INSERT_WATCHED_MOVIES, (viewer, title))


def get_watched_movies(viewer):
    with connection:
        curse = connection.cursor()
        curse.execute(SELECT_WATCHED_MOVIES, (viewer, ))
        return curse.fetchall()
