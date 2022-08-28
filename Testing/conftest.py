import pytest
import sys, os

sys.path.append(os.path.join('..', 'MusicManager'))
from MusicManager import MusicManager

sys.path.append(os.path.join('..', 'Database'))
from DatabaseManager import DatabaseManager

import ytdl_options

def pytest_configure():
    pytest.saveloc_test = "saveloc_test"
    pytest.yt_url = "https://www.youtube.com/watch?v=2fngvQS_PmQ"
    pytest.yt_url_songname = "I See Fire (Music Video)"
    pytest.yt_url_artist = "Ed Sheeran"
    pytest.yt_url_unsplittable = "https://www.youtube.com/watch?v=hRr7qRb-7k4"

    pytest.db_path = "Database/testDB"

@pytest.fixture
def music_manager():
    mm = MusicManager(ytdl_options)
    return mm

@pytest.fixture
def db_manager():
    dm = DatabaseManager(pytest.db_path)
    return dm
