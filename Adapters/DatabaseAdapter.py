import sys, os

sys.path.append(os.path.join('..', 'MusicManager'))
import Song

sys.path.append(os.path.join('..', 'Database'))
from DatabaseManager import DatabaseManager

# This class adapts the DatabaseManager class to the MusicManager.
class DatabaseAdapter:
    def __init__(self, db_path: str = 'SongsDatabase') -> None:
        self.db_manager = DatabaseManager(db_path)

    def add_genre(self, genre):
        genre = genre.upper()

        query = f'INSERT INTO Genres VALUES(\'{genre}\')'
        self.db_manager.write(query)
        # TBE

    def add_song(self, song):
        query = f'INSERT INTO Songs VALUES(\'{song.title}\', \'{song.artist}\', \'{song.genre}\', \'{song.path}\')'
        self.db_manager.write(query)
        # TBE
    
    def genre_exists(self, genre) -> bool:
        query = f'SELECT COUNT(1) FROM Genres WHERE name = \'{genre}\''
        cursor = self.db_manager.read(query)
        records = cursor.fetchone()

        return False if records == 0 else True

    # Fetches a random song from the database.
    def fetch_song(self, genre) -> Song:
        if self.genre_exists(genre):
            query = f'SELECT * FROM Songs ORDER BY RAND() LIMIT 1'
            cursor = self.db_manager.write(query)
        
            print(cursor.fetchall())
            return None
        
        # genre doesn't exist exception TBE
        return None

