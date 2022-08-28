import pytest
import youtube_dl as ytdl
import sys, os

sys.path.append(os.path.join('..', 'MusicManager'))

from Song import Song

"""
Trying to download a song using a wrong url
raises a ytdl.utils.DownloadError exception.
"""
def test_download_song_wrong_url_raise_exc(music_manager):
    url = "unavailableurl"
    save_loc = pytest.saveloc_test

    with pytest.raises(ytdl.utils.DownloadError):
        music_manager.download_song(url = url, save_location = save_loc)

"""
Trying to download a song using a location
that doesn't exist raises a OSError exception.
"""
def test_save_song_inexistent_location_raise_exc(music_manager):
    url = pytest.yt_url 
    save_loc = "wrongloc"

    with pytest.raises(OSError):
        music_manager.download_song(url = url, save_location = save_loc)

"""
Trying to split the title of the video (using '-' as sep)
might not always be possible. In that case, the value of
artist should be 'Unknown' by default.
"""
@pytest.mark.yt_download
def test_title_cannot_be_split_artist_unknown(music_manager):
    url = pytest.yt_url_unsplittable
    save_loc = pytest.saveloc_test

    song = music_manager.get_song_info(url = url, save_location = save_loc)
    assert song.artist == 'Unknown'

"""
When the title of the video can be splitted,
the artist and the name of the song should be separated.
"""
@pytest.mark.yt_download
def test_title_can_be_split_artist_and_song_known(music_manager):
    url = pytest.yt_url
    save_loc = pytest.saveloc_test

    song = music_manager.get_song_info(url = url, save_location = save_loc)

    assert song.title == pytest.yt_url_songname
    assert song.artist == pytest.yt_url_artist


"""
Testing the download_song method. We give a valid, splittable url 
as input and a valid save location.
"""
@pytest.mark.yt_download
def test_download_song(music_manager):
    url = pytest.yt_url
    save_loc = pytest.saveloc_test

    song = music_manager.download_song(url = url, save_location = save_loc)

    assert os.path.exists(f'{save_loc}/{song.title}, {song.artist}.mp3')


"""
Testing the add_song method. We give a music genre as input
and keep the default values for search_limit and location.
"""
@pytest.mark.yt_download
def test_add_song(music_manager):
    genre = "kazi ploae"
    save_loc = pytest.saveloc_test
    song = music_manager.add_song(genre, save_location = save_loc)

    assert os.path.exists(f'{save_loc}/{song.title}, {song.artist}.mp3')

"""
Testing the add_song method when giving a genre (here, a random string) that doesn't return
any playlist.
"""
@pytest.mark.yt_download
def test_add_song_no_results(music_manager):
    genre = "xclkxznmcvoisdnjfoiksdaj"
    save_loc = pytest.saveloc_test


    with pytest.raises(Exception):
        song = music_manager.add_song(genre, save_location = save_loc)

    
