from math import modf

from flask import jsonify
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

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
    yt_song_id = Column(String)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    artist_id = Column(Integer, ForeignKey('artist.id'))
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
    artist = relationship("Artist", back_populates = "songs")

    def to_json(self):
        return jsonify({
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "duration": (lambda song_duration_fract, song_duration_int: f'{int(song_duration_int)}:{int(round(song_duration_fract, 2) * 60)}')(*modf(self.duration_minutes))
        })
    
class Artist(Base):
    __tablename__ = 'artist'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    
    # This relationships links the artist to song
    songs = relationship("Song", back_populates = "artist")