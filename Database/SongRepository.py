from sqlalchemy.orm import session
from datetime import datetime, timedelta

from Database.models import Genre, Song


"""
This variable helps evaluate whether a song should remain in the playlist based on recent listening patterns.

The algorithm as a whole works as follows:
Each listening cycle tracks user engagement with songs. 
At the end of each cycle, the current_cycle_play_count resets, allowing for a fresh measurement of user interest 
in the next cycle.

To determine if a song should be removed, we compare recent listening behavior with past engagement. 
Here, "present" refers to a one-week period, while "past" encompasses all previous listening history.

If a song that hasn't been played for some time begins to get played again but continues to show 
low engagement (indicated by a low average listening time both in the current and past cycles) it 
will be removed from the playlist. This approach helps ensure that the playlist stays filled with 
songs that consistently provide a positive listening experience.
"""
LISTENING_CYCLE_LENGTH = datetime.timedelta(weeks = 1)

"""
Minimum accepted distance between the current listening cycle and the last
time a song has been listened to outside of the current cycle. Minimum accepted
means that we are only into consideration the deletion of a song if this criteria is respected.
"""
MINIMUM_DISTANCE_BETWEEN_LISTENINGS = datetime.timedelta(weeks = 3)

"""
Minimum average listening time percentage.
"""
MINIMUM_AVG_LISTENING_TIME = 0.2

"""
How much can be current cycle can be compared to the past in terms of listening percentage.
"""
REMOVAL_THRESHOLD_RATIO = 0.7

"""
Minimum accepted play count for the current cycle in order to consider a song for deletion.
"""
MINIMUM_CURRENT_CYCLE_PLAY_COUNT = 5

class SongRepository:
    def __init__(self, session: session):
        self.session = session
    
    def add_song(self, yt_playlist_id: str, yt_song_id: str, genre_id: int, title: str, duration_seconds: int) -> None:
        song = Song(
            yt_playlist_id = yt_playlist_id,
            yt_song_id = yt_song_id,
            genre_id = genre_id,
            title = title,
            last_listened = None,
            last_listened_percent = None,
            duration_seconds = duration_seconds,
            play_count = 0
        )
        
        self.session.add(song)
        self.session.commit()
        
    def clear_song_list(self) -> None:
        self.session.query(Song).filter(
            Song.current_cycle_play_count > MINIMUM_CURRENT_CYCLE_PLAY_COUNT and 
            Song.average_listen_time / Song.duration_seconds < MINIMUM_AVG_LISTENING_TIME and 
            # Song.average_listen_time / Song.duration_seconds - Song.average_listen_time_before_cycle / Song.duration_seconds > REMOVAL_THRESHOLD_RATIO and
            Song.last_listened - Song.last_listened_before_cycle > MINIMUM_DISTANCE_BETWEEN_LISTENINGS
            )
    
    def update_song_play_count(self, song: Song) -> None:
        if song:
            song.play_count += 1
            self.session.commit()
    
    def get_genre_by_name(self, genre_name: str) -> Genre:
        return self.session.query(Genre).filter(Genre.name == genre_name).first()
    
    