import sqlite3

conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS song_artist;")
cursor.execute("DROP TABLE IF EXISTS artist;")
cursor.execute("DROP TABLE IF EXISTS song;")
cursor.execute("DROP TABLE IF EXISTS genre;")

cursor.execute('''
    CREATE TABLE genre (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE song (
        id INTEGER PRIMARY KEY,
        yt_playlist_id TEXT,
        yt_song_id TEXT,
        genre_id INTEGER,
        title TEXT NOT NULL,
        duration_minutes INTEGER,
        last_played_before_cycle DATETIME,
        last_played DATETIME,
        play_time_minutes_before_cycle FLOAT,
        play_time_minutes FLOAT,
        average_play_time_minutes_before_cycle FLOAT,
        average_play_time_minutes FLOAT,
        play_count_before_cycle INTEGER,
        play_count INTEGER,
        FOREIGN KEY (genre_id) REFERENCES genre(id) ON DELETE SET NULL
    );
''')

cursor.execute('''
    CREATE TABLE artist (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE song_artist (
        song_id INTEGER,
        artist_id INTEGER,
        PRIMARY KEY (song_id, artist_id),
        FOREIGN KEY (song_id) REFERENCES song(id) ON DELETE CASCADE,
        FOREIGN KEY (artist_id) REFERENCES artist(id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()

print("Database 'songs.db' and tables created successfully.")