import random
import subprocess
import os
import threading
import time 

from ytmusicapi import YTMusic

from Database.models import Song
from Database.SongRepository import SongRepository

class MusicManager:
    def __init__(self):
        self.yt = YTMusic()
        self.song_repo = SongRepository()
        self.is_playing = False
        
        self.audio_thread= None
        self.audio_thread_interrupt_signal = None
        
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
    
    def yt_fetch_song(self, genre: str) -> str:
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
                path = song_path
            )
            
            if not add_ok:
                os.remove(download_path)
            
        else:
            print('Error: Download failed.')
    
    def restart_play_cycle(self) -> None:
        pass
    
    def refresh_song_list(self) -> None:
        pass
    
    def play_mpg123(interrupt_signal, song_path):
        process = subprocess.Popen(['mpg123', song_path])
        
        while not interrupt_signal:
            time.sleep(0.1)
            
        process.terminate()
    
    def play(self, song: Song) -> None:
        if self.is_playing:
            return False
    
        self.thread_interrupt_signal = threading.Event()
        self.audio_thread = threading.Thread(target = self.play_mpg123, args={song.path})
        self.audio_thread.start()
    
    def stop(self) -> None:
        if not self.is_playing:
            return True
    
        self.thread_interrupt_signal.set()
        self.audio_thread.join()
        
        self.audio_thread = None
        self.audio_thread_interrupt_signal = None

    def next(self, next_song: Song) -> None:
        self.stop()
        self.play(next_song)
        

        
    