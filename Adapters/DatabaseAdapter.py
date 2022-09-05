import sys, os

from MusicManager.Song import Song
from Database.DatabaseManager import DatabaseManager

# This class adapts the DatabaseManager class to the MusicManager.
class DatabaseAdapter:
    def __init__(self, db_path: str = 'SongsDatabase') -> None:
        self.db_manager = DatabaseManager(db_path)

    def add_genre(self, genre):
        query = f'INSERT INTO Genres VALUES("{genre}")'
        self.db_manager.write(query)
        # TBE

    def add_song(self, song):
        query = f'INSERT INTO Songs VALUES("{song.title}", "{song.artist}", "{song.genre}", "{song.path}", datetime("now"))'
        self.db_manager.write(query)
        # TBE
    
    def genre_exists(self, genre) -> bool:
        query = f'SELECT COUNT(1) FROM Genres WHERE name = "{genre}"'
        records = self.db_manager.read(query)
        records = records[0][0]

        return False if records == 0 else True

    # Fetches a random song from the database.
    def fetch_song(self, genre) -> Song:
        if self.genre_exists(genre):
            query = f'SELECT * FROM Songs ORDER BY RANDOM() LIMIT 1'
            db_song = self.db_manager.write(query)
            
            if len(db_song) == 0:
                print('Failure: There is no song from this genre!')
                return None
            
            db_song = db_song[0]
            song = Song(db_song[0], db_song[1], db_song[2], db_song[3])

            return song
        
        print('Failure: The specified genre does not exist!')
        return None
