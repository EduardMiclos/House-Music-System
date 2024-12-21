from math import modf

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_apscheduler import APScheduler
from flask_cors import CORS

from BluetoothManager.BluetoothManager import BluetoothManager
from MusicManager.MusicManager import MusicManager

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
scheduler = APScheduler()

class MusicSystem:
    def __init__(self) -> None:
        self.emissions = 0

        # The MAC address of the bluetooth speaker.
        self.bluetooth_device = "2C:FD:B4:38:5D:CA"
        self.music_manager = MusicManager()
        self.bluetooth_manager = BluetoothManager(self.bluetooth_device)

ms = MusicSystem()

@scheduler.task("cron", id="job_maintain_bluetooth_connection", second="15")
def maintain_bluetooth_connection():

    with scheduler.app.app_context():
        print('[CRON] Checking bluetooth connection...')

        if not ms.bluetooth_manager.is_connected():
            print("[CRON] Bluetooth device is not connected.")
            ms.bluetooth_manager.connect()

        bluetooth_json = {
            'status': 'connected' if ms.bluetooth_manager.is_connected() else 'connecting',
            'device': ms.bluetooth_manager.get_device_name() if ms.bluetooth_manager.is_connected() else None
        }

        socketio.emit('bluetooth', bluetooth_json)

@socketio.on('connect')
def connect():
    print(f'Connected: {request.sid}')

    bluetooth_json = {
        'status': 'connected' if ms.bluetooth_manager.is_connected() else 'connecting',
        'device': ms.bluetooth_manager.get_device_name() if ms.bluetooth_manager.is_connected() else None
    }

    emit('bluetooth', bluetooth_json, to=request.sid)

# @app.route('/playsong', methods=['GET'])
# def playsong():
#     ms.music_manager.play(genre = "romantic")

# @app.route('/pausesong', methods=['GET'])
# def pausesong():
#     ms.music_manager.stop()

@app.route('/recently-played', methods=['GET'])
def get_recently_played():
    recently_played_songs = ms.music_manager.song_repo.get_recently_played_songs()

    return jsonify({
        "songs": [
            {
                'title': song.title,
                'artist': song.artist.name,
                'duration': (lambda song_duration_fract, song_duration_int: f'{int(song_duration_int)}:{int(round(song_duration_fract, 2) * 60)}')(*modf(song.duration_minutes))
            }
            for song in recently_played_songs
        ]
    })


@app.route('/songs', methods=['GET'])
def get_songs():
    song_title = request.args.get('title')

    if not song_title:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    songs = ms.music_manager.song_repo.get_songs_by_name(song_title)
    if not songs:
        return jsonify({"error": "No songs were found"}, 404)

    return jsonify({
        "songs": [
            {
                'title': song.title,
                'artist': song.artist.name,
                'genre': song.genre
            }
            for song in songs
        ]
    }), 200

@app.route('/play', methods=['POST'])
def play_song():
    data = request.json
    song_id = data.get('song_id', None)

    if song_id is not None:
        song = ms.music_manager.song_repo.get_song_by_id(song_id)
        ms.music_manager.play(song = song)
        return jsonify({"status": "playing"}), 200
    else:
        return jsonify({"error": "Invalid request. Please provide a song id."}), 400

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()

    socketio.run(app, host='0.0.0.0', port=5001, debug=False)