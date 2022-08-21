import youtube_dl as ytdl
from youtubesearchpython import PlaylistsSearch
import os
from typing import List

class MusicManager:
    def __init__(self, ytdl_options: dict) -> None:
        self.ytdl_options = ytdl_options

    # Refreshes the list of songs.
    def full_refresh(self) -> None:
        pass

    # Only refreshes the hits.
    def refresh_hits(self) -> None:
        pass

    # Adds a new song to the database.
    # THIS MIGHT RECEIVE A 'SONG' OBJECT AS PARAMETER!!!!
    def add_song(self, genre: str, search_limit: int = 5) -> None:

        search_query = genre + ' playlist'
        playlists_search = PlaylistsSearch(search_query, limit = search_limit)

        # All the resulted playlists
        playlist = playlist_search.result()['result']

        # Getting a random playlist from the lists of playlists

        # Getting a random link from the specific playlist
        
        # Downloading the song and saving it to the specified location     

#videosSearch = PlaylistsSearch('kazi ploae playlist', limit = 2)

#playlist = videosSearch.result()['result'][1]['link']

#import youtube_dl

#with youtube_dl.YoutubeDL(ytdl_options) as ydl:
#    playlist_dict = ydl.extract_info(playlist, download = False)

#    for video in playlist_dict["entries"]:
#        print(video.get("title"))


    #https://stackoverflow.com/questions/44183473/get-video-information-from-a-list-of-playlist-with-youtube-dl
        

    # Returns the name of the song, the artist (if it can be determined) and the path to the song inside the machine.
    def get_song_info(self, url: str, save_location: str) -> List[str]:

        # Gets the title (song name and artist).
        with ytdl.YoutubeDL(self.ytdl_options) as ytdl_configured:

            # Extracts video information
            video_info = ytdl_configured.extract_info(url, download = False)

            song_name = None

            # If the name of the artist cannot be determined, the default value is 'Unknown'.
            artist = "Unknown"

            try: 
                title = video_info.get("title", None)
                song_path = save_location + '/' + title
                title = title.split('-')

                artist, song_name = title
            except ValueError:
                print('Warning: The name of the artist couldn\'t be determined. Default to: Unknown')
                song_name = title

        return [song_name, artist, song_path]



    # Downloads a song with the specified url and saves the .mp3 to save_location.
    def download_song(self, url: str, save_location: str) -> List[str]: 
   
        # Checks to see if the directory exists.
        if not os.path.isdir(save_location):
            raise OSError('Error: The specified location does not exist!')

        # WE DEFINITELY NEED A SONG CLASS   
        song_name, artist, song_path = self.get_song_info(url = url, save_location = save_location)

        # The dot at the end is mandatory in order to avoid some errors.
        self.ytdl_options['outtmpl'] = song_path + '.'
        with ytdl.YoutubeDL(self.ytdl_options) as ytdl_configured:
            ytdl_configured.download([url])
           
        return [song_name, artist, song_path]
