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
            "DOWNLOAD": ['download new songs', self.download]
        }

        self.db_adapter = DatabaseAdapter('Database/SongsDatabase.db')
        self.music_manager = MusicManager()
        self.voice_adapter = VoiceCommandAdapter(voice_cmds = self.voice_cmds.items())

    def play_genre(self) -> None:
        pass

    def play_song(self) -> None:
        pass

    def full_refresh(self) -> None:
        pass

    def refresh_hits(self) -> None:
        pass

    def download(self) -> None:
        pass



