import random
import subprocess
import os
import threading
import time 

from ytmusicapi import YTMusic

from Database.models import Song, Genre
from Database.SongRepository import SongRepository

# tbd add chronjob for refreshing song cycle

class MusicManager:
    def __init__(self):
        self.yt = YTMusic()
        self.song_repo = SongRepository()
        
        # A single song can be played at once.
        self.current_genre = None
        self.current_song = None
        self.current_song_play_time_in_minutes = None
        self.is_playing = False
        self.should_play = False
    
        self.music_thread = None
        self.music_thread_interrupt_signal = None
        
        self.audio_thread = None
        self.audio_thread_interrupt_signal = None 

        self.initialize()
        
    # Downloads a song with the specified url and saves the .mp3 to save_location.
    def download_song(self, url: str, save_location: str, song_id: str) -> str: 
        output_template = f'{save_location}/{song_id}.%(ext)s'
        
        command = [
            'yt-dlp',
            '--extract-audio',
            '--audio-format', 'mp3',
            url,
            '-o', output_template
        ]
        
        try:
            subprocess.run(command,
                           check = True, 
                           text = True, 
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE
                          )
            
            output_file = f'{save_location}/{song_id}.mp3'
            
            if os.path.exists(output_file):
                return output_file
            return None
        except subprocess.CalledProcessError as e:
            print(f'Error: {e.stderr}')
            return None
    
    def yt_fetch_song(self, genre: str) -> None:
        all_yt_ids = self.song_repo.get_all_yt_ids()
        genre = self.song_repo.get_genre_by_name(genre)
        
        if genre is None:
            return None
        
        yt_search = self.yt.search(f"popular {genre.name} playlist")
        all_playlists = [result for result in yt_search if result['resultType'] == 'playlist']
        
        selected_song_id = None 
        while selected_song_id is None:
            random_playlist = random.choice(all_playlists)
            
            if 'playlistId' in random_playlist:
                playlist_id = random_playlist['playlistId']
                playlist = self.yt.get_playlist(playlist_id)
        
                tracks = playlist['tracks']
                
                while selected_song_id is None:
                    random_track = random.choice(tracks)
                    
                    if 'videoId' in random_track:
                        yt_id = random_track['videoId']
                        
                        if yt_id not in all_yt_ids:
                            selected_song_id = yt_id
        
        song = self.yt.get_song(selected_song_id)
        song_path = f'Database/songs/{genre.id}'    
        
        download_path = self.download_song(
            url = song['microformat']['microformatDataRenderer']['urlCanonical'], 
            save_location = song_path,
            song_id = selected_song_id)
        
        if download_path is not None:
            add_ok = self.song_repo.add_song(
                yt_playlist_id = playlist_id,
                yt_song_id = selected_song_id,
                genre_id = genre.id,
                title = song['videoDetails']['title'],
                duration_minutes = int(song['videoDetails']['lengthSeconds']) / 60,
                author_name = song['videoDetails']['author'],
                path = f'{song_path}/{selected_song_id}.mp3'
            )
            
            if not add_ok:
                os.remove(download_path)
            
        else:
            print('Error: Download failed.')
    
    def restart_play_cycle(self) -> None:
        self.song_repo.restart_cycle()
    
    def refresh_song_list(self) -> None:
        self.song_repo.cleanup_songs()
        
        all_genres = self.song_repo.get_all_genres()
        for genre in all_genres:
            self.yt_fetch_song(genre.name)

    def shuffle_song(self) -> Song:
        if self.current_genre is not None:
            return self.song_repo.get_random_song_by_genre(self.current_genre)

    def audio_thread_exec(self, song_path):
        self.is_playing = True
        play_start_time = time.time()
        
        process = subprocess.Popen(
            ['mpg123', song_path],
            stdin = subprocess.PIPE,
            
            # detaching mpg123 from the terminal
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL)
         
        while not self.audio_thread_interrupt_signal.is_set() and process.poll() is None:
            time.sleep(0.1)
        
        if self.audio_thread_interrupt_signal.is_set():
            process.terminate()
            process.wait()

        play_end_time = time.time()
        
        self.current_song_play_time_in_minutes = (play_end_time - play_start_time) / 60

        self.is_playing = False
        self.current_song = None

    def music_thread_exec(self): 

        def should_play_next_song():
            return self.should_play is True and self.is_playing is False
        
        def should_shuffle_next_song():
            return self.current_song is None

        def clear_audio_thread():
            self.audio_thread_interrupt_signal.set()
            self.audio_thread.join()

            self.audio_thread_interrupt_signal.clear()
            self.audio_thread = None

        while True:
            if should_play_next_song():
                if self.audio_thread is not None:
                    clear_audio_thread()

                if should_shuffle_next_song():
                    self.current_song = self.shuffle_song()

                self.audio_thread = threading.Thread(target = self.audio_thread_exec, args = {self.current_song.path})
                self.audio_thread.start()

            if self.music_thread_interrupt_signal.is_set():
                if self.audio_thread is not None:
                    clear_audio_thread()

                self.music_thread_interrupt_signal.clear()

            time.sleep(1)

    def initialize(self) -> None:
        self.audio_thread_interrupt_signal = threading.Event()
        self.music_thread_interrupt_signal = threading.Event()

        self.music_thread = threading.Thread(target = self.music_thread_exec)
        self.music_thread.start()

    # tbd: change genre from str to actual Genre class and make the verification in upper class
    def play(self, song: Song = None, genre: str = None) -> None:
        if not self.is_playing:
            if song is not None:
                self.current_song = song
            if genre is not None:
                self.current_genre = self.song_repo.get_genre_by_name(genre)

            self.should_play = True

    def pause(self) -> None:
        if self.is_playing:
            self.should_play = False
            self.music_thread_interrupt_signal.set()

    def next(self, song: Song = None) -> None:
        self.stop()
        self.play(song)
        
    