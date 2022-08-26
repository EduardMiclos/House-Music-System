import youtube_dl as ytdl
from youtubesearchpython import PlaylistsSearch
import os
from typing import List
import random
from Song import Song

class MusicManager:
    def __init__(self, ytdl_options: dict) -> None:
        self.ytdl_options = ytdl_options


    # Refreshes the list of songs.
    def full_refresh(self) -> None:
        pass


    # Only refreshes the hits.'https://www.youtube.com/watch?v=lp-EO5I60KA'
    def refresh_hits(self) -> None:
        pass


    # Adds a new song to the database.
    # Source: https://stackoverflow.com/questions/44183473/get-video-information-from-a-list-of-playlist-with-youtube-dl
    def add_song(self, genre: str, search_limit: int = 5, save_location: str = os.environ["SONGS"]) -> Song:

        search_query = f'{genre} music' 
        playlists_search = PlaylistsSearch(search_query, limit = search_limit)

        # Fetches all the resulted playlists.
        playlists = playlists_search.result()['result']

        if len(playlists) == 0:
            raise Exception("Failure: No playlists was found!")

        # Gets the link of a random playlist from the lists of playlists.
        playlist = random.choice(playlists)['link']

        with ytdl.YoutubeDL(self.ytdl_options) as ytdl_configured:
            playlist_dict = ytdl_configured.extract_info(playlist, download = False)
            playlist_dict = playlist_dict['entries']

            # Gets a random id from the specific playlist.
            yt_id = random.choice(playlist_dict)['id']

            # Generates the YT URL.
            yt_url = f'https://www.youtube.com/watch?v={yt_id}'

            # Downloads the song and saves it to the specified location.
            song = self.download_song(url = yt_url, save_location = save_location)

            return song

        return None



    # Returns a song object.
    def get_song_info(self, url: str, save_location: str) -> Song:

        # Creates a new, empty song object.
        song = Song()

        # Gets the title (song name and artist).
        with ytdl.YoutubeDL(self.ytdl_options) as ytdl_configured:

            # Extracts video information.
            video_info = ytdl_configured.extract_info(url, download = False)

            try: 
                yt_full_title = video_info.get("title", None)
                yt_full_title_splitted = yt_full_title.split('-')

                song.artist = yt_full_title_splitted[0]
                song.title = yt_full_title_splitted[1:]

                song.artist = ' '.join(song.artist).strip()
                song.title = ' '.join(song.title).strip()
            except ValueError:
                print('Warning: The name of the artist couldn\'t be determined. Default to: Unknown')
                song.title = yt_full_title

        song.path = f'{save_location}/{song.title}, {song.artist}'
        return song



    # Downloads a song with the specified url and saves the .mp3 to save_location.
    def download_song(self, url: str, save_location: str) -> List[str]: 
   
        # Checks to see if the directory exists.
        if not os.path.isdir(save_location):
            raise OSError('Error: The specified location does not exist!')

        song = self.get_song_info(url = url, save_location = save_location)

        # The dot at the end is mandatory in order to avoid some errors.
        self.ytdl_options['outtmpl'] = song.path + '.'
        with ytdl.YoutubeDL(self.ytdl_options) as ytdl_configured:
            ytdl_configured.download([url])
           
        return song
