import pytest
import youtube_dl as ytdl

from MusicManager.ytdl_options import ytdl_options
from MusicManager.MusicManager import MusicManager

@pytest.fixture
def music_manager():
    musicManager = MusicManager(ytdl_options)
    return musicManager


def test_cannot_save_song_when_location_doesnt_exist(music_manager):
    url = 'https://www.youtube.com/watch?v=lp-EO5I60KA'
    save_location = 'inexistent_directory'

    with pytest.raises(OSError):
        music_manager.download_song(url = url, save_location = save_location)

def test_cannot_download_song_with_wrong_url(music_manager):
    url = 'https://www.youtube.com/watch?v=lp-wrongURL'
    save_location = 'test_location'

    with pytest.raises(ytdl.utils.DownloadError):
        music_manager.download_song(url = url, save_location = save_location)

@pytest.mark.skip(reason='This takes too long')
def test_artist_unknown_when_title_cannot_be_split(music_manager):
    url = 'https://www.youtube.com/watch?v=RBumgq5yVrA'
    save_location = 'test_location'

    _, artist, _ = music_manager.download_song(url = url, save_location = save_location)
    assert artist == 'Unknown'



