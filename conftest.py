import pytest
from MusicManager.MusicManager import MusicManager
from MusicManager.ytdl_options import ytdl_options

def pytest_configure():
    pytest.saveloc_test = "MusicManager/saveloc_test"
    pytest.wrong_saveloc = "wrongloc"
    pytest.yt_url = "https://www.youtube.com/watch?v=2fngvQS_PmQ"
    pytest.yt_url_songname = "I See Fire (Music Video)"
    pytest.yt_url_artist = "Ed Sheeran"
    pytest.yt_url_unsplittable = "https://www.youtube.com/watch?v=hRr7qRb-7k4"
    pytest.yt_url_unavailable = "unavailableurl"

@pytest.fixture
def music_manager():
    musicManager = MusicManager(ytdl_options)
    return musicManager


