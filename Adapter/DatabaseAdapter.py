import sys, os

sys.path.append(os.path.join('..', 'MusicManager'))

from MusicManager import Song

# This class adapts the DatabaseManager class to the MusicManager.
class DatabaseAdapter:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_genre(self, genre):
        query = f'INSERT INTO Genres VALUES(\'{genre}\')'
        self.db_manager.write(query)

    def add_song(self, song):
        query = f'INSERT INTO Genres VALUES(\'{song.title}\', \'{song.artist}\', \'{song.genre}\', \'{song.path}\')'
        self.db_manager.write(query)
    
    # Fetches a random song from the database.
    def fetch_song(self) -> Song:
        pass




    
