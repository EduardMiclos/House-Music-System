from Adapters.VoiceCommandAdapter import VoiceCommandAdapter
from MusicManager.MusicManager import MusicManager


class MusicSystem:
    def __init__(self) -> None:
        # List of the UUIDs of all the available Bluetooth Devices.
        self.bluetooth_devices =  {
            "JBL_GO3_1": '2C:FD:B4:38:5D:CA',
            "JBL_GO3_2": '', # Need to buy it first.
            "MICROPHONE_UUID": '' # Need to but it first.
        }

        # List of all the voice commands along with the corresponding function pointers.
        self.voice_cmds = {
            "PLAY_GENRE": ['play genre', self.play_genre],
            "PLAY_SONG": ['play song', self.play_song],
            "FULL_REFRESH": ['make a full refresh', self.full_refresh],
            "HITS_REFRESH": ['refresh the hits', self.refresh_hits],
            "DOWNLOAD": ['download new songs', self.download],
            "PAUSE": ['pause', self.pause],
            "STOP": ['stop', self.stop],
            "TURN_OFF": ['turn off', self.turn_off]
        }

        self.music_manager = MusicManager()
        self.voice_adapter = VoiceCommandAdapter(voice_cmds = self.voice_cmds.items())

    def play_genre(self) -> None:
        self.voice_adapter.speak('Please pick a genre')

    def play_song(self) -> None:
        self.voice_adapter.speak('Please pick a song')

    def full_refresh(self) -> None:
        self.voice_adapter.speak('Refreshing all songs')

    def refresh_hits(self) -> None:
        self.voice_adapter.speak('Refreshing all the hits')

    def download(self) -> None:
        self.voice_adapter.speak('Downloading new songs')

    def pause(self) -> None:
        self.voice_adapter.speak('Pausing')

    def stop(self) -> None:
        self.voice_adapter.speak('Stopping')

    def turn_off(self) -> None:
        self.voice_adapter.speak('Turning off. Goodbye!')


ms = MusicSystem()
ms.voice_adapter.interpret("downgrade new ong")()
