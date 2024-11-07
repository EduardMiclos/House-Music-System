from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = 'sqlite:///songs.db'

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

song_artist_association = Table(
    'song_artist',
    Base.metadata,
    Column('song_id', Integer, ForeignKey('song.id', ondelete='CASCADE'), primary_key=True),
    Column('artist_id', Integer, ForeignKey('artist.id', ondelete='CASCADE'), primary_key=True)
)

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
    yt_song_id = Column(String)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    title = Column(String, nullable = False)
    duration_minutes = Column(Integer)
    last_played_before_cycle = Column(DateTime)
    last_played = Column(DateTime)
    play_time_minutes_before_cycle = Column(Float)
    play_time_minutes = Column(Float)
    average_play_time_minutes_before_cycle = Column(Float)
    average_play_time_minutes = Column(Float)
    play_count_before_cycle = Column(Integer)
    play_count = Column(Integer)
    path = Column(String)
    
    # Linking the song both to a genre and to one or more artists
    genre = relationship("Genre", back_populates = "songs")
    artists = relationship("artist", secondary = song_artist_association, back_populates = "song")
    
class Artist(Base):
    __tablename__ = 'artist'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    
    # Linking the artist to a song
    song = relationship("Song", secondary = song_artist_association, back_populates = "artists")

# Now, creating all the tables in the database
Base.metadata.create_all(engine)

# Creating a session maker to manage database sessions
Session = sessionmaker(bind = engine)
session = Session()