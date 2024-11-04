import sqlite3

conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

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
        last_listened_before_cycle DATETIME,
        last_listened DATETIME,
        average_listen_time_before_cycle FLOAT,
        average_listen_time FLOAT,
        duration_seconds INTEGER,
        current_cycle_play_count INTEGER,
        FOREIGN KEY (genre_id) REFERENCES genre(id)
    );
''')

cursor.execute('''
    CREATE TABLE artist (
        id INTEGER PRIMARY KEY,
        song_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (song_id) REFERENCES song(id)
    );
''')

conn.commit()
conn.close()

print("Database 'songs.db' and tables created successfully.")