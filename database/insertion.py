from audio.tools import read_binary_file, get_audio_duration
from database.creation import get_connection
from database.helper import get_artist_id_by_name, get_album_id_by_title
from pathlib import Path


def add_artist(name: str, bio: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO artists (name, bio)
                       VALUES (?, ?)
                       """,
                       (name, bio))


def add_album(artist: str, title: str, release_year: int, cover_image_path: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        artist_id = get_artist_id_by_name(artist)
        cover_image_bin = read_binary_file(cover_image_path)

        cursor.execute("""
                       INSERT INTO albums (artist_id, title, release_year, cover_image)
                       VALUES (?, ?, ?, ?)
                       """,
                       (artist_id, title, release_year, cover_image_bin))


def add_album_track(artist: str, title: str, release_year: int, music_file_path: str, album: str,
                    cover_image_path: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        artist_id = get_artist_id_by_name(artist)
        album_id = get_album_id_by_title(album, artist)
        music_file_bin = read_binary_file(music_file_path)
        duration_seconds = get_audio_duration(music_file_path)
        cover_image_bin = read_binary_file(cover_image_path)

        # Add the track itself
        cursor.execute("""
                       INSERT INTO tracks (artist_id, title, duration_seconds, release_year, music_file, cover_image)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """,
                       (artist_id, title, duration_seconds, release_year, music_file_bin, cover_image_bin))

        track_id = cursor.lastrowid

        # Assign track to album
        cursor.execute("""
                       INSERT INTO album_tracks (album_id, track_id)
                       VALUES (?, ?)
                       """,
                       (album_id, track_id))


def add_single_track(artist: str, title: str, release_year: int, music_file_path: str, cover_image_path: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        artist_id = get_artist_id_by_name(artist)
        music_file_bin = read_binary_file(music_file_path)
        duration_seconds = get_audio_duration(music_file_path)
        cover_image_bin = read_binary_file(cover_image_path)

        cursor.execute("""
                       INSERT INTO tracks (artist_id, title, duration_seconds, release_year, music_file, cover_image)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """,
                       (artist_id, title, duration_seconds, release_year, music_file_bin, cover_image_bin))


def initialize_database(base_bath: str = "../database/data"):
    base = Path(base_bath)

    for artist_folder in base.iterdir():
        # Skip if not a directory
        if not artist_folder.is_dir():
            continue
        artist_name = artist_folder.name
        bio_file = artist_folder / "bio.txt"
        bio = bio_file.read_text(encoding="utf-8").strip() if bio_file.exists() else None

        # Insert artist
        add_artist(artist_name, bio)

        for album_folder in artist_folder.iterdir():
            # Skip if not a directory
            if not album_folder.is_dir():
                continue

            if album_folder.name == "singles":
                # todo: Should initialize singles, but after the artist has been added to db
                continue

            ## Handling Album
            if '-' not in album_folder.name:
                print(f"Skipped {artist_name}->{album_folder.name} because it does not contain release year.")
                continue

            *album_parts, year = album_folder.name.rsplit('-', 1)
            album_title = '-'.join(album_parts)  # maybe strip?

            try:
                release_year = int(year)
            except ValueError:
                print(f"Skipped {artist_name}->{album_folder.name} because release year is not an integer.")
                continue

            cover_image = album_folder / f"{album_title}.jpg"
            if not cover_image.exists():
                print(f"Missing album cover in {artist_name}->{album_folder.name}.")
                continue

            # Insert Album
            add_album(artist=artist_name, title=album_title, release_year=release_year,
                      cover_image_path=str(cover_image))

            # Handle tracks
            for track_file in album_folder.iterdir():

                if track_file.name == f"{album_title}.jpg":
                    continue  # Skip album cover

                track_title = track_file.stem
                try:
                    add_album_track(
                        artist=artist_name,
                        title=track_title,
                        release_year=release_year,
                        music_file_path=str(track_file),
                        album=album_title,
                        cover_image_path=str(cover_image)
                    )
                except Exception as e:
                    print(f"Error while adding track {artist_name}->{album_folder.name}->{track_file.name}: {e}")


if __name__ == '__main__':
    initialize_database()
