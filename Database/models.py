from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = 'sqlite:///songs.db'

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Genre(Base):
    __tablename__ = 'genre'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    
    # This relationships links the songs with a genre
    songs = relationship("Song", back_populates = "genre")
    
class Song(Base):
    __tablename__ = 'song'
    
    id = Column(Integer, primary_key = True)
    yt_playlist_id = Column(String, nullable = False)
    yd_song_id = Column(String)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    title = Column(String, nullable = False)    
    last_listened_before_cycle = Column(DateTime)
    last_listened = Column(DateTime)
    average_listen_time_before_cycle = Column(Float)
    average_listen_time = Column(Float)
    duration_seconds = Column(Integer)
    current_cycle_play_count = Column(Integer)
    
    # Linking the song both to a genre and to one or more artists
    genre = relationship("Genre", back_populates = "songs")
    artists = relationship("artist", back_populates = "song")
    
class Artist(Base):
    __tablename__ = 'artist'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    
    # Linking the artist to a song
    song = relationship("Song", back_populates = "artists")

# Now, creating all the tables in the database
Base.metadata.create_all(engine)

# Creating a session maker to manage database sessions
Session = sessionmaker(bind = engine)
session = Session()