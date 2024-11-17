import sqlite3
import os
import shutil

conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS song_artist;")
cursor.execute("DROP TABLE IF EXISTS artist;")
cursor.execute("DROP TABLE IF EXISTS song;")
cursor.execute("DROP TABLE IF EXISTS genre;")

cursor.execute('''
    CREATE TABLE genre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE song (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        yt_playlist_id TEXT,
        yt_song_id TEXT,
        genre_id INTEGER,
        title TEXT NOT NULL,
        artist_id TEXT NOT NULL,
        duration_minutes INTEGER,
        last_played_before_cycle DATETIME,
        last_played DATETIME,
        play_time_minutes_before_cycle FLOAT,
        play_time_minutes FLOAT,
        average_play_time_minutes_before_cycle FLOAT,
        average_play_time_minutes FLOAT,
        play_count_before_cycle INTEGER,
        play_count INTEGER,
        path TEXT NOT NULL,
        FOREIGN KEY (genre_id) REFERENCES genre(id) ON DELETE SET NULL
    );
''')

cursor.execute('''
    CREATE TABLE artist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
''')

GENRES = [
    'romantic',
    'rock',
    'pop',
    'hip-hop',
    'disco',
    'manele'
]

if os.path.exists('songs'):
        shutil.rmtree('songs')
os.mkdir('songs')
        
for genre in GENRES:
    cursor.execute(f'''INSERT INTO genre (name) VALUES ('{genre}')''')
    os.mkdir(f'songs/{cursor.lastrowid}')


conn.commit()
conn.close()

print("Database 'songs.db' and tables created successfully.")