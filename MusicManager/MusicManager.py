
import sys, os
import youtube_dl as ytdl
from youtubesearchpython import PlaylistsSearch, VideosSearch
from typing import List
import random

from Song import Song
import ytdl_options

sys.path.append(os.path.join('..', 'Adapters'))
from DatabaseAdapter import DatabaseAdapter

class MusicManager:
    def __init__(self, ytdl_options: dict, db_adapter: DatabaseAdapter = DatabaseAdapter()) -> None:
        self.ytdl_options = ytdl_options
        self.db_adapter = db_adapter

    # Refreshes the list of songs.
    def full_refresh(self) -> None:
        pass


    # Only refreshes the hits.
    def refresh_hits(self) -> None:
        pass


    def __get_playlist_link(self, search_query, search_limit):
        playlists_search = PlaylistsSearch(search_query, limit = search_limit)

        # Fetches the resulted playlists.
        playlists = playlists_search.result()['result']

        if len(playlists) == 0:
            raise Exception("Failure: No playlists was found!")

        # Gets the link of a random playlist from the lists of playlists.
        playlist = random.choice(playlists)['link']

        return playlist

    def __get_song_link(self, search_query):
        videos_search = VideosSearch(search_query, limit = 1)

        # Fetches the resulted videos.
        videos = videos_search.result()['result']

        if len(videos) == 0:
            raise Exception("Failure: No song was found!")

        video = videos[0]['link']

        return video


    def __fetch_song(self, playlist) -> Song:
        with ytdl.YoutubeDL(self.ytdl_options.playlist) as ytdl_configured:
            playlist_dict = ytdl_configured.extract_info(playlist, download = False)
            playlist_dict = playlist_dict['entries']

            # Gets a random id from the specific playlist.
            yt_id = random.choice(playlist_dict)['id']

            # Generates the YT URL.
            yt_url = f'https://www.youtube.com/watch?v={yt_id}'

            # Downloads the song and saves it to the specified location.
            song = self.download_song(url = yt_url, save_location = save_location)

            return song


    # Adds a new song to the database.
    # Source: https://stackoverflow.com/questions/44183473/get-video-information-from-a-list-of-playlist-with-youtube-dl
    def add_song(self, genre: str = None, title: str = None, url: str = None, search_limit: int = 5, save_location: str = "../Database/songs") -> Song:

        song = None

        if genre is not None:
            # Getting a randomly selected playlist.
            playlist = self.__get_playlist_link(genre, search_limit)

            # Fetching a randomly selected song from the playlist.
            song = self.__fetch_song(playlist)  
        elif title is not None:
            # Getting the song url.
            song_url = self.__get_song_link(title)

            # Downloading the song.
            song = self.download_song(url = song_url, save_location = save_location)
        elif url is not None:
            # Directly downloading the song.
            song = self.download_song(url = url, save_location = save_location)
        else:
            print('Failure: You need to specify either a genre, a title or the url for a specific song!')

        if song is not None:
            # Adding the song to the database.
            self.db_adapter.add_song(song)
    
        return song



    # Returns a song object.
    def get_song_info(self, url: str, save_location: str) -> Song:

        # Creates a new, empty song object.
        song = Song()

        # Gets the title (song name and artist).
        with ytdl.YoutubeDL(self.ytdl_options.video) as ytdl_configured:

            # Extracts video information.
            video_info = ytdl_configured.extract_info(url, download = False)

            yt_title = video_info.get("title", None)
            if '-' in yt_title:
                yt_title = yt_title.split('-')

                song.artist = yt_title[0]

                song.title = yt_title[1:]
                song.title = ''.join(song.title).strip()
            else:
                print('Warning: The name of the artist couldn\'t be determined. Default to: Unknown')
                song.title = yt_title
 
        song.lower()
        song.path = f'{save_location}/{song.title}, {song.artist}'
        return song



    # Downloads a song with the specified url and saves the .mp3 to save_location.
    def download_song(self, url: str, save_location: str) -> List[str]: 
   
        # Checks to see if the directory exists.
        if not os.path.isdir(save_location):
            raise OSError('Error: The specified location does not exist!')

        song = self.get_song_info(url = url, save_location = save_location)

        # The dot at the end is mandatory in order to avoid some errors.
        self.ytdl_options.video['outtmpl'] = song.path + '.'
        with ytdl.YoutubeDL(self.ytdl_options.video) as ytdl_configured:
            ytdl_configured.download([url])
           
        return song
