import os
import datetime

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_apscheduler import APScheduler
from flask_cors import CORS

from BluetoothManager.BluetoothManager import BluetoothManager
from MusicManager.MusicManager import MusicManager

load_dotenv()
app = Flask(__name__)
CORS(app)

# Socketio instance for efficient websocket communication.
# This is required in order to sync multiple web instances, due to the fact that multiple users can open multiple browser sessions
# but there is a single raspberry pi & JBL speaker on the system. 
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
scheduler = APScheduler()

# cached songs that are currently displayed on front-end (current song playing + recently played songs + listed songs after search)
playing_song_cache = None
recently_played_songs_cache = {}
searched_songs_cache = {}

class MusicSystem:
    def __init__(self) -> None:
        self.emissions = 0

        # The MAC address of the bluetooth speaker.
        self.bluetooth_device = os.getenv('SPEAKER_MAC_ADDRESS')
        self.music_manager = MusicManager()
        self.bluetooth_manager = BluetoothManager(self.bluetooth_device)

ms = MusicSystem()

# Creating a scheduled task that runs every 15 seconds and checks the bluetooth connection to the JBL Speaker.
# If the current status is different from the previous status, send a message through websocket to all the frontend instances.
@scheduler.task("interval", id="job_maintain_bluetooth_connection", seconds=15)
def maintain_bluetooth_connection():

    def connection_status_has_changed():
        previous_is_connected = ms.bluetooth_manager.is_connected
        current_is_connected = ms.bluetooth_manager.check_if_connected()

        # update the current connection status
        ms.bluetooth_manager.is_connected = current_is_connected

        if current_is_connected != previous_is_connected:
            return True
        return False

    with scheduler.app.app_context():
        print(f'[CRON {datetime.datetime.now()}] Checking bluetooth connection...')

        if not ms.bluetooth_manager.check_if_connected():
            print(f'[CRON {datetime.datetime.now()}] Bluetooth device is not connected.')
            ms.bluetooth_manager.try_connect()
        else:
            print(f'[CRON {datetime.datetime.now()}] Bluetooth device is connected.')

        if connection_status_has_changed():
            print(f'[CRON {datetime.datetime.now()}] Bluetooth connection status has changed. Announcing FE.')

            if ms.bluetooth_manager.is_connected:
                bluetooth_json = {
                'status': 'connected',
                'device': ms.bluetooth_manager.get_device_name()
                }
            else:
                bluetooth_json = {
                'status': 'connecting',
                'device': None
                }

            socketio.emit('bluetooth', bluetooth_json)

def update_cache(song_cache_json, song_objects):
    for song_obj in song_objects:
        song_cache_json[str(song_obj.id)] = song_obj

@socketio.on('connect')
def connect():
    print(f'Connected: {request.sid}')

    bluetooth_json = {
        'status': 'connected' if ms.bluetooth_manager.is_connected else 'connecting',
        'device': ms.bluetooth_manager.get_device_name() if ms.bluetooth_manager.is_connected else None
    }

    playing_json = {
        'is_playing': ms.music_manager.is_playing,
        'song': ms.music_manager.current_song.to_json() if ms.music_manager.current_song is not None else None
    }

    app_state_json = {
        'bluetooth_state': bluetooth_json,
        'playing_state': playing_json
    }

    # informing the recently connected device in regards to the application current state
    emit('app_state', app_state_json, to = request.sid)

@app.route('/recently-played', methods=['GET'])
def get_recently_played():
    global recently_played_songs_cache
    recently_played_songs_cache = {}

    recently_played_songs = ms.music_manager.song_repo.get_recently_played_songs()

    if not recently_played_songs:
        return jsonify({
                "error": "No songs were found"
                }), 404

    update_cache(recently_played_songs_cache, recently_played_songs)

    return jsonify({
        "songs": [
            song.to_json() 
            for song in recently_played_songs
        ]
    }), 200

@app.route('/songs', methods=['GET'])
def get_songs():
    global searched_songs_cache
    searched_songs_cache = {}

    song_title = request.args.get('title')
    if not song_title:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    songs = ms.music_manager.song_repo.get_songs_by_title(song_title)
    if not songs:
        return jsonify({"error": "No songs were found"}, 404)

    update_cache(searched_songs_cache, songs)

    return jsonify({
        "songs": [
            song.to_json() 
            for song in songs
        ]
    }), 200

# tbd: set-up a cache for storing all the songs that are currently displayed
# on frontend and instantly get the song from that cache list (search by id) [use redis-json]
@app.route('/play', methods=['POST'])
def play_song():
    global playing_song_cache, recently_played_songs_cache

    if not ms.bluetooth_manager.check_if_connected():
        return jsonify({
            "error": "Bluetooth is not connected."
        }), 400

    data = request.json
    song_id = data.get('song_id', None)

    if song_id is not None and song_id > 0:

        # first search the song in cache
        if playing_song_cache is not None and song_id == playing_song_cache.id:
            song = playing_song_cache
        elif str(song_id) in recently_played_songs_cache:
            song = recently_played_songs_cache[str(song_id)]
        elif str(song_id) in searched_songs_cache:
            song = searched_songs_cache[str(song_id)]

        # fallback to database
        else:
            song = ms.music_manager.song_repo.get_song_by_id(song_id)

        if song is None:
            return jsonify({"error": "Could not find song."}), 500 

        playing_song_cache = song
        ms.music_manager.play(song = song)

        # tbd send socket message to update state [maybe abstract the emit method]
        return jsonify({"status": "playing", "song": song.to_json()}), 200
    else:
        return jsonify({"error": "Invalid request. Please provide a song id."}), 400
    
@app.route('/pause', methods=['POST'])
def pause_song():
    if not ms.bluetooth_manager.check_if_connected():
        return jsonify({
            "error": "Bluetooth is not connected."
        }), 400

    ms.music_manager.pause()

    # tbd send socket message to update state [maybe abstract the emit method]
    return jsonify({
        "status": "paused", 
        "song": ms.music_manager.current_song.to_json()
        }), 200

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()

    socketio.run(app, host='0.0.0.0', port=5001, debug=False)