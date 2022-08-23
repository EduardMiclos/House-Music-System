import pytest
import youtube_dl as ytdl
from MusicManager.Song import Song

"""
Trying to download a song using a wrong url
raises a ytdl.utils.DownloadError exception.
"""
def test_download_song_wrong_url_raise_exc(music_manager):
    url = pytest.yt_url_unavailable
    save_loc = pytest.saveloc_test

    with pytest.raises(ytdl.utils.DownloadError):
        music_manager.download_song(url = url, save_location = save_loc)

"""
Trying to download a song using a location
that doesn't exist raises a OSError exception.
"""
def test_save_song_inexistent_location_raise_exc(music_manager):
    url = pytest.yt_url 
    save_loc = pytest.wrong_saveloc

    with pytest.raises(OSError):
        music_manager.download_song(url = url, save_location = save_loc)

"""
Trying to split the title of the video (using '-' as sep)
might not always be possible. In that case, the value of
artist should be 'Unknown' by default.
"""
@pytest.mark.skip(reason='This may take too long')
def test_title_cannot_be_split_artist_unknown(music_manager):
    url = pytest.yt_url_unsplittable
    save_location = pytest.saveloc_test

    song = music_manager.get_song_info(url = url, save_location = save_location)
    assert song.artist == 'Unknown'

"""
When the title of the video can be splitted,
the artist and the name of the song should be separated.
"""
@pytest.mark.skip(reason='This may take too long')
def test_title_can_be_split_artist_and_song_known(music_manager):
    url = pytest.yt_url
    save_location = pytest.saveloc_test

    song = music_manager.get_song_info(url = url, save_location = save_location)

    assert song.title == pytest.yt_url_songname and song.artist == pytest.yt_url_artist



