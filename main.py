#from MusicManager.MusicManager import MusicManager

#from typing import List
from MusicManager.ytdl_options import ytdl_options
from MusicManager.MusicManager import MusicManager


musicManager = MusicManager(ytdl_options = ytdl_options)
#musicManager.download_song(url="https://www.youtube.com/watch?v=q2a1m-tQrGU", save_location='.')
musicManager.add_song('kazi ploae')

#from youtubesearchpython import PlaylistsSearch

#videosSearch = PlaylistsSearch('kazi ploae playlist', limit = 2)

#playlist = videosSearch.result()['result'][1]['link']

#import youtube_dl

#with youtube_dl.YoutubeDL(ytdl_options) as ydl:
    #playlist_dict = ydl.extract_info(playlist, download = False)

    #print(playlist_dict['entries'][0]['id'])
