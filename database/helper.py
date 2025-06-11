from database.creation import get_connection


def get_artist_id_by_name(name: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        artist_id = cursor.execute(
            "SELECT id FROM artists WHERE name = ?",
            (name,)
        ).fetchone()[0]

        return artist_id


def get_album_id_by_title(title: str, artist: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        artist_id = get_artist_id_by_name(artist)
        album_id = cursor.execute(
            "SELECT id FROM albums WHERE title = ? AND artist_id = ?",
            (title, artist_id)
        ).fetchone()[0]

        return album_id
