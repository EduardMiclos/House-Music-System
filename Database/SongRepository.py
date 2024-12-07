import random
from typing import List

from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from Database.models import Genre, Song, Artist


"""
This variable helps evaluate whether a song should remain in the playlist based on recent playing patterns.

The algorithm as a whole works as follows:
Each playing cycle tracks user engagement with songs. 
At the end of each cycle, the current_cycle_play_count resets, allowing for a fresh measurement of user interest 
in the next cycle.

To determine if a song should be removed, we compare recent listening behavior with past engagement. 
Here, "present" refers to a one-week period, while "past" encompasses all previous playing history.

If a song that hasn't been played for some time begins to get played again but continues to show 
low engagement (indicated by a low average listening time both in the current and past cycles) it 
will be removed from the playlist. This approach helps ensure that the playlist stays filled with 
songs that consistently provide a positive playing experience.
"""
PLAYING_CYCLE_LENGTH = timedelta(weeks = 1)

"""
Minimum accepted distance between the current playing cycle and the last
time a song has been played to outside of the current cycle. Minimum accepted
means that we are only into consideration the deletion of a song if this criteria is respected.
"""
MINIMUM_DISTANCE_BETWEEN_PLAYINGS = timedelta(weeks = 3)

"""
Minimum average playing time percentage.
"""
MINIMUM_AVG_PLAYING_TIME = 0.2

"""
How much can be current cycle can be compared to the past in terms of playing percentage.
"""
REMOVAL_THRESHOLD_RATIO = 0.7

"""
Minimum accepted play count for the current cycle in order to consider a song for deletion.
"""
MINIMUM_CURRENT_CYCLE_PLAY_COUNT = 5

class SongRepository:
    def __init__(self, engine: str = 'sqlite:///Database/songs.db'):
        self.engine = create_engine(engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
    
    def add_song(self, yt_playlist_id: str, yt_song_id: str, genre_id: int, title: str, duration_minutes: int, author_name: str, path: str) -> bool:
        artist = self.session.query(Artist).filter(Artist.name == author_name).first()
        
        if artist is None:
            artist = Artist(name = author_name)
            self.session.add(artist)
            self.session.commit()
    
        existing_song = self.session.query(Song).filter(
            or_(
                Song.yt_song_id == yt_song_id,
                and_(
                    Song.title == title,
                    Song.artist == artist
                )
            )
        ).first()
        
        if existing_song:
            return False
    
        song = Song(
            yt_playlist_id = yt_playlist_id,
            yt_song_id = yt_song_id,
            genre_id = genre_id,
            artist_id = artist.id,
            title = title,
            duration_minutes = duration_minutes,
            last_played_before_cycle = None,
            last_played = None,
            play_time_minutes_before_cycle = None,
            play_time_minutes = None,
            average_play_time_minutes_before_cycle = None,
            average_play_time_minutes = None,
            play_count_before_cycle = None,
            play_count = None,
            path = path
        )
        
        self.session.add(song)
        self.session.commit()
        
        return True
    
    def restart_cycle(self) -> None:
        self.session.query(Song).update({
            Song.last_played_before_cycle: Song.last_played,
            
            Song.play_count_before_cycle: Song.play_count_before_cycle + Song.play_count,
            Song.play_time_minutes_before_cycle: Song.play_time_minutes_before_cycle + Song.play_time_minutes,
            
            Song.average_play_time_minutes_before_cycle: (
                (Song.play_time_minutes_before_cycle + Song.play_time_minutes) / 
                (Song.play_count_before_cycle + Song.play_count)
            ) if (Song.play_count_before_cycle + Song.play_count) > 0 else 0,
            
            Song.play_count: 0,
            Song.play_time_minutes: 0,
            Song.average_play_time_minutes: 0
            })
        self.session.commit()
        
    def cleanup_songs(self) -> None:
        has_minimum_plays = Song.play_count > MINIMUM_CURRENT_CYCLE_PLAY_COUNT
        low_engagement = (
            Song.average_play_time_minutes / Song.duration_minutes <= MINIMUM_AVG_PLAYING_TIME
            if Song.duration_minutes > 0 else False
        )
        declining_interest = (
            (
                Song.average_play_time_minutes / Song.duration_minutes - 
                Song.average_play_time_minutes_before_cycle / Song.duration_minutes
            ) > REMOVAL_THRESHOLD_RATIO
            if Song.duration_minutes > 0 else False
        )
        sufficent_time_gap = Song.last_played - Song.last_played_before_cycle > MINIMUM_DISTANCE_BETWEEN_PLAYINGS
        
        self.session.query(Song).filter(
            has_minimum_plays,
            low_engagement,
            declining_interest,
            sufficent_time_gap
            ).delete(synchronize_session=False) 
        
        self.session.commit()
    
    def update_song_at_play(self, song: Song) -> None:
        if song:
            song.last_played = datetime.now()
            self.session.commit()

    def update_song_at_change(self, song: Song, current_session_play_time_minutes: float) -> None:
        if song:
            song.play_count += 1
            song.play_time_minutes += min(song.duration_minutes, current_session_play_time_minutes)
            song.average_play_time_minutes = song.play_time_minutes / song.play_count
            self.session.commit()
            
    def get_all_yt_ids(self, ) -> object:
        return self.session.query(Song).with_entities(Song.yt_song_id).all()
    
    def get_genre_by_name(self, genre_name: str) -> Genre:
        return self.session.query(Genre).filter(Genre.name == genre_name).first()
    
    def get_random_song_by_genre(self, genre: Genre) -> Song:
        songs = self.session.query(Song).filter(Song.genre_id == genre.id).all()
    
        if songs:
            return random.choice(songs)
        
    def get_all_genres(self) -> List[Genre]:
        return self.session.query(Genre).all()