import os
import sqlite3

DB_PATH = "../database.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_artist_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS artists
                       (
                           id   INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL UNIQUE,
                           bio  TEXT DEFAULT NULL
                       );
                       """)


def create_track_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS tracks
                       (
                           id               INTEGER PRIMARY KEY AUTOINCREMENT,
                           artist_id        INTEGER NOT NULL,
                           title            TEXT    NOT NULL,
                           duration_seconds INTEGER NOT NULL,
                           release_year     INTEGER NOT NULL,
                           music_file       BLOB    NOT NULL,
                           cover_image      BLOB    DEFAULT NULL,
                           is_favorite      INTEGER DEFAULT 0 CHECK ( is_favorite IN (0, 1) ),
                           FOREIGN KEY (artist_id) REFERENCES artists (id)
                       );
                       """)


def create_album_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS albums
                       (
                           id           INTEGER PRIMARY KEY AUTOINCREMENT,
                           artist_id    INTEGER NOT NULL,
                           title        TEXT    NOT NULL,
                           release_year INTEGER NOT NULL,
                           cover_image  BLOB DEFAULT NULL,
                           FOREIGN KEY (artist_id) REFERENCES artists (id)
                       );
                       """)


def create_playlist_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS playlists
                       (
                           id   INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL DEFAULT 'New Playlist'
                       );
                       """)


# Mapping Tables

def create_album_tracks_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS album_tracks
                       (
                           album_id INTEGER NOT NULL,
                           track_id INTEGER NOT NULL,
                           PRIMARY KEY (album_id, track_id),
                           FOREIGN KEY (album_id) REFERENCES albums (id),
                           FOREIGN KEY (track_id) REFERENCES tracks (id)
                       );
                       """)


def create_playlist_tracks_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS playlist_tracks
                       (
                           playlist_id INTEGER NOT NULL,
                           track_id    INTEGER NOT NULL,
                           PRIMARY KEY (playlist_id, track_id),
                           FOREIGN KEY (playlist_id) REFERENCES playlists (id),
                           FOREIGN KEY (track_id) REFERENCES tracks (id)
                       );
                       """)


def create_database():
    create_artist_table()
    create_track_table()
    create_album_table()
    create_playlist_table()
    create_album_tracks_table()
    create_playlist_tracks_table()


def reset():
    print("Did you close DataBase Connection?")
    response = input("Enter Y/N: ")
    if response.lower() != "y":
        return

    print("WARNING: This will delete the database file.")
    response = input("Are You Sure? Enter Y/N: ")
    if response.lower() != "y":
        return

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Database file deleted.")
        create_database()
        print("Database reset successful.")
    else:
        print("Database file does not exist.")
        return


if __name__ == '__main__':
    reset()
