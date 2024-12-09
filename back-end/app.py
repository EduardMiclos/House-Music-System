import threading
from time import sleep

from flask import Flask, request, jsonify
from flask_socketio import SocketIO

from BluetoothManager.BluetoothManager import BluetoothManager
from MusicManager.MusicManager import MusicManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

class MusicSystem:
    def __init__(self) -> None:
        self.emissions = 0

        # The MAC address of the bluetooth speaker.
        self.bluetooth_device = "2C:FD:B4:38:5D:CA"
        self.music_manager = MusicManager()
        self.bluetooth_manager = BluetoothManager(self.bluetooth_device)

        self.initialize_bluetooth_connection()
    
    def maintain_bluetooth_connection(self) -> None:
        while True:
            print(f'SHOULD EMIT DISCONNECTED! {self.emissions}')
            # self.emissions += 1

            socketio.emit('bluetooth', {'status': 'connecting', 'device': None})

            # while not self.bluetooth_manager.is_connected():
            #     self.bluetooth_manager.connect()
            #     sleep(2)

            sleep(10)

            print(f'SHOULD EMIT CONNECTED! {self.emissions}')
            socketio.emit('bluetooth', {'status': 'connected', 'device': self.bluetooth_manager.get_device_name()})
            # self.emissions += 1

            # while self.bluetooth_manager.is_connected():
            #     sleep(0.5)

            sleep(10)
    
    def initialize_bluetooth_connection(self) -> None:
        bluetooth_connection_thread = threading.Thread(target = self.maintain_bluetooth_connection, daemon = True)
        bluetooth_connection_thread.start()

ms = MusicSystem()

@socketio.on('connect')
def on_join():
    bluetooth_json = {
        'status': 'connected' if ms.bluetooth_manager.is_connected() else 'connecting',
        'device': ms.bluetooth_manager.get_device_name() if ms.bluetooth_manager.is_connected() else None
    }

    socketio.emit('bluetooth', bluetooth_json, to=request.sid)

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
                'artist': song.artist,
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
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)